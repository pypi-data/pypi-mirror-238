import os
import uuid
from io import BytesIO
from typing import Dict, List, NoReturn, Tuple

import arrow
import nibabel as nib
import numpy as np
import SimpleITK as sitk
from neolibrary.monitoring.logger import NeoLogger
from PIL import Image
from skimage.transform import resize

log = NeoLogger(__name__)
ROOT = os.getcwd()

class ThumbnailCreator:
    """ThumbnailCreator is a class for creating thumbnails from the image."""

    def get_plane_dims(self, spacing: List[float], plane: int) -> Tuple[float, float]:
        """Get the dimensions of the plane.

        Parameters
        ----------
        spacing : list
            The spacing of the image.
        plane : int
            The plane to get the dimensions of.

        Returns
        -------
        col_dim : float
            The column dimension of the plane.
        row_dim : float
            The row dimension of the plane.
        """
        try:
            log.info("Getting plane dimensions")
            if plane == 3:
                col_dim, row_dim = spacing[0], spacing[1]
            elif plane == 2:
                col_dim, row_dim = spacing[0], spacing[2]
            elif plane == 1:
                col_dim, row_dim = spacing[1], spacing[2]
            else:
                raise ValueError("Invalid plane value")

            log.success("Plane dimensions fetched")
            return col_dim, row_dim
        except (ValueError, IndexError) as e:
            log.error(f"Error getting plane dimensions: {e}")
        except Exception as e:
            log.error(f"Unexpected error getting plane dimensions: {e}")

    def resize_and_transform(self, img_shape: List[int], spacing: List[float], thumbnail_slice: np.ndarray, axis: int = 0) -> np.ndarray:
        """Resize and transform the image.

        Parameters
        ----------
        img_shape : list
            The shape of the image.
        spacing : list
            The spacing of the image.
        thumbnail_slice : np.ndarray
            The thumbnail slice to resize and transform.
        axis : int, optional
            The axis to resize and transform, by default 0.

        Returns
        -------
        resized_slice : np.ndarray
            The resized and transformed slice.

        Returns
        -------
        np.ndarray
            The resized and transformed slice.
        """
        try:
            log.info("Resizing and transforming image")
            container_width = img_shape[0]
            container_height = img_shape[1]

            col_dim, row_dim = self.get_plane_dims(spacing, axis + 1)
            cols, rows = thumbnail_slice.shape[0], thumbnail_slice.shape[1]
            
            print(f"axis: {axis}")
            print(f"thumbnail_slice.shape: {thumbnail_slice.shape}")
            print(f"cols: {cols}, rows: {rows}")
            print(f"col_dim: {col_dim}, row_dim: {row_dim}")

            ratio_cols_rows = cols / rows
            ratio_rows_cols = rows / cols

            ratio_cols_rows_pix_dims = col_dim / row_dim
            ratio_rows_cols_pix_dims = row_dim / col_dim

            ratio_cols_rows *= ratio_cols_rows_pix_dims
            ratio_rows_cols *= ratio_rows_cols_pix_dims

            canvas_width = container_width * ratio_cols_rows
            canvas_height = container_height

            # set longest dimension to container width/height and resize other dimension accordingly
            if canvas_width > canvas_height:
                canvas_height = container_height * ratio_rows_cols
                canvas_width = container_width

            upscaled_canvas_width = round(canvas_width)
            upscaled_canvas_height = round(canvas_height)
        
            resized_slice = resize(thumbnail_slice, (upscaled_canvas_width, upscaled_canvas_height), mode="constant", anti_aliasing=True)
            log.success(f"=> Image resized and transformed from ({rows}, {cols}) => ({upscaled_canvas_height}, {upscaled_canvas_width})")
            return resized_slice
        except (ValueError, IndexError) as e:
            log.error(f"Error resizing and transforming image: {e}")
        except Exception as e:
            log.error(f"Unexpected error resizing and transforming image: {e}")

    def make_uint(self, img: np.ndarray) -> np.ndarray:
        """Make the image uint8.

        Parameters
        ----------
        img : np.ndarray
            The image to make uint8.

        Returns
        -------
        np.ndarray
            The uint8 image.
        """
        try:
            minimum = np.min(img)
            newimg = img - minimum
            maximum = np.max(newimg)
            newimg = newimg / maximum
            newimg = newimg * 255
            newimg = newimg.astype(np.uint8)
            return newimg
        except (ValueError, IndexError) as e:
            log.error(f"Error making image uint8: {e}")
        except Exception as e:
            log.error(f"Unexpected error making image uint8: {e}")

    def most_segmented(self, msk: np.ndarray, axis: int = 0) -> int:
        """Get the most segmented slice.

        Parameters
        ----------
        msk : np.ndarray
            The mask to get the most segmented slice from.
        axis : int, optional
            The axis to get the most segmented slice from, by default 0.

        Returns
        -------
        int
            The most segmented slice.
        """
        try:
            log.info("Fetching most segmented slice index")
            axis_view = [(1, 2), (0, 2), (0, 1)]
            unique_classes = np.unique(msk)
            log.info(f"Unique classes: {unique_classes}")
            if len(msk.shape) != 3:
                raise ValueError("Mask must be 3D (If image is slice 2D, add an extra empty dimension)")
            if len(unique_classes) > 2:
                log.info("Mask is multiclass, assuming equal weight to all classes and find slice with most segmentation")
                msk = msk.copy()
                msk[msk > 1] = 1
            if len(unique_classes) == 1:
                log.warning("Mask only contains one value, mask is probably empty")
            else:
                log.info("Mask is binary, finding slice with most segmentation")
            relevant_slice = np.argmax(np.sum(msk, axis=axis_view[axis]))
            log.success(f"=> Most segmented slice index is {relevant_slice} for axis {axis}")
            return relevant_slice
        except (ValueError, IndexError) as e:
            log.error(f"Error fetching most segmented slice index: {e}")

        except Exception as e:
            log.error(f"Unexpected error fetching most segmented slice index: {e}")

    def transform_rgb_array(self, relevant_slice: int, img_arr: np.ndarray, msk_arr: np.ndarray | None = None, axis: int = 0) -> np.ndarray:
        """Transform the RGB array.

        Parameters
        ----------
        relevant_slice : int
            The relevant slice.
        img_arr : np.ndarray
            The image array.
        msk_arr : np.ndarray
            The mask array.
        axis : int, optional
            The axis to transform the RGB array, by default 0.

        Returns
        -------
        np.ndarray
            The transformed RGB array.
        """
        try:
            log.info("Transforming RGB array")
            first_dim = 0
            second_dim = 1
            msk_arr = msk_arr.copy().astype("int") if msk_arr is not None and msk_arr.any() else None
            x = img_arr.shape[0]
            y = img_arr.shape[1]
            z = img_arr.shape[2]
            thumbnail_slice = np.zeros((y, z, 3)) if axis == first_dim else np.zeros((x, z, 3)) if axis == second_dim else np.zeros((x, y, 3)) # This is flipped, axis 0 should be axis 2, axis 2 should be axis 1
            # this function expects image shape (x, y, z)
            if axis == first_dim:
                thumbnail_slice[:, :, 0] = self.make_uint(img_arr[relevant_slice, :, :])
                thumbnail_slice[:, :, 1] = self.make_uint(img_arr[relevant_slice, :, :])
                thumbnail_slice[:, :, 2] = self.make_uint(img_arr[relevant_slice, :, :])
                seg_slice = msk_arr[relevant_slice, :, :] if msk_arr is not None and msk_arr.any() else None

            elif axis == second_dim:
                thumbnail_slice[:, :, 0] = self.make_uint(img_arr[:, relevant_slice, :])
                thumbnail_slice[:, :, 1] = self.make_uint(img_arr[:, relevant_slice, :])
                thumbnail_slice[:, :, 2] = self.make_uint(img_arr[:, relevant_slice, :])
                seg_slice = msk_arr[:, relevant_slice, :] if msk_arr is not None and msk_arr.any() else None

            else:
                thumbnail_slice[:, :, 0] = self.make_uint(img_arr[:, :, relevant_slice])
                thumbnail_slice[:, :, 1] = self.make_uint(img_arr[:, :, relevant_slice])
                thumbnail_slice[:, :, 2] = self.make_uint(img_arr[:, :, relevant_slice])
                seg_slice = msk_arr[:, :, relevant_slice] if msk_arr is not None and msk_arr.any() else None
            log.success("=> Transformed image slice into RGB")
            return thumbnail_slice, seg_slice
        except (ValueError, IndexError) as e:
            log.error(f"Error transforming RGB array: {e}")
        except Exception as e:
            log.error(f"Unexpected error transforming RGB array: {e}")

    def overlay_rgb_mask(
            self,
            thumbnail_slice: np.ndarray,
            msk_arr: np.ndarray | None,
            labels: Dict[str, str],
            seg_slice: np.ndarray,
            opacity: float = 0.6) -> np.ndarray:
        """Overlay the RGB mask.

        Parameters
        ----------
        thumbnail_slice : np.ndarray
            The thumbnail slice.
        msk_arr : np.ndarray | None
            The mask array.
        labels : Dict[str, str]
            The labels.
        seg_slice : np.ndarray
            The segmentation slice.
        opacity : float, optional
            The opacity, by default 0.6.

        Returns
        -------
        np.ndarray
            The overlayed RGB mask.
        """
        try:
            log.info("Overlaying RGB mask")
            if msk_arr is not None:
                for counter, label in enumerate(labels):
                    colorhex = label["color"]
                    colormap = self.hex_to_rgba(colorhex)
                    counter += 1 # bypass background
                    thumbnail_slice[:, :, 0][seg_slice == counter] = thumbnail_slice[:, :, 0][seg_slice == counter] * (1 - opacity) + opacity * colormap[0]
                    thumbnail_slice[:, :, 1][seg_slice == counter] = thumbnail_slice[:, :, 1][seg_slice == counter] * (1 - opacity) + opacity * colormap[1]
                    thumbnail_slice[:, :, 2][seg_slice == counter] = thumbnail_slice[:, :, 2][seg_slice == counter] * (1 - opacity) + opacity * colormap[2]
            log.success("=> RGB mask overlayed")
            return thumbnail_slice
        except (ValueError, IndexError) as e:
            log.error(f"Error overlaying RGB mask: {e}")
        except Exception as e:
            log.error(f"Unexpected error overlaying RGB mask: {e}")

    def create_img(
            self,
            img_arr: np.ndarray,
            spacing: List[float],
            labels: Dict[str, str | int],
            axis: int = 0,
            msk_arr: np.ndarray = None,
            img_shape: List[int] = [500, 500],
            opacity: float = 0.6) -> np.ndarray:
        """Create the image.

        Parameters
        ----------
        img_arr : np.ndarray
            The image array.
        msk_arr : np.ndarray
            The mask array.
        spacing : list
            The spacing of the image.
        labels : dict
            The labels of the image.
        axis : int, optional
            The axis to create the image from, by default 0.
        img_shape : list, optional
            The shape of the image, by default [500, 500].
        opacity : float, optional
            The opacity of the mask, by default 0.6.

        Returns
        -------
        np.ndarray
            The image.
        """
        try:
            log.info(f"Creating image with axis {axis}")
            if msk_arr is not None:
                relevant_slice = self.most_segmented(msk_arr, axis=axis)
            else:
                log.info("No mask provided, assuming middle slice is most relevant")
                relevant_slice = img_arr.shape[axis] // 2  # Since we have no mask we assume the middle slice is the most relevant
            thumbnail_slice, seg_slice = self.transform_rgb_array(relevant_slice=relevant_slice, img_arr=img_arr, msk_arr=msk_arr, axis=axis)
            thumbnail_slice = self.overlay_rgb_mask(thumbnail_slice=thumbnail_slice, msk_arr=msk_arr, labels=labels, seg_slice=seg_slice, opacity=opacity)
            thumbnail_slice = self.resize_and_transform(img_shape=img_shape, spacing=spacing, thumbnail_slice=thumbnail_slice, axis=axis)
            log.success("=> Image slice created successfully")
            return thumbnail_slice
        except (ValueError, AttributeError) as e:
            log.error(f"Could not create image slice: {e}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")

    def convert_to_hex(self, img: np.ndarray, _format: str = "jpeg") -> str:
        """Converts an image to a hex string.

        Parameters
        ----------
        img : np.ndarray
            The image to convert.
        _format : str, optional
            The _format of the image, by default "jpeg".

        Returns
        -------
        str
            The hex string.
        """
        try:
            log.info("Converting image to hex")
            buf = BytesIO()
            if img.dtype != np.uint8:
                log.warning(f"Image is {type(img)} and not of the expected type uint8, trying to convert, but this might cause problems")
                img = img.astype(np.uint8)
            image = Image.fromarray(img)
            image.save(buf, format=_format)
            buf.seek(0)
            hex_values = buf.getvalue().hex()
            log.success("=> Image converted to hex")
            return hex_values
        except (ValueError, AttributeError) as e:
            log.error(f"Could not convert image to hex: {e}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")

    def convert_all_axes_to_hex(
            self,
            imgs_dict: Dict[str, np.ndarray],
            _format: str = "jpeg") -> Dict[str, str]:
        """Converts all images to hex strings.

        Parameters
        ----------
        imgs_dict : dict
            The images to convert.
        _format : str, optional
            The _format of the images, by default "jpeg".

        Returns
        -------
        dict
            The hex strings.
        """
        try:
            log.info("Converting images to hex")
            output = {}
            for image_slice_dim in imgs_dict:
                output[image_slice_dim] = self.convert_to_hex(imgs_dict[image_slice_dim], _format=_format)
            log.success("=> Successfully converted all axes images converted to hex")
            return output
        except (ValueError, AttributeError) as e:
            log.error(f"Could not convert images to hex: {e}")

    def thumbnail_all_axis(
            self,
            image: np.ndarray,
            spacing: List[float],
            labels: Dict[str, str | int] = None,
            mask: np.ndarray = None,
            opacity: float = 0.6) -> Dict[str, np.ndarray]:
        """Creates a thumbnail for each axis.

        Parameters
        ----------
        image : np.ndarray
            The image array.
        mask : np.ndarray
            The mask array.
        spacing : list
            The spacing of the image.
        labels : dict
            The labels of the image.

        Returns
        -------
        Dict[str, np.ndarray]
            The thumbnails in the _format {"dim_1": np.ndarray, "dim_2": np.ndarray, "dim_3": np.ndarray}.
        """
        try:
            # log.info("Reversing spacings")
            # spacing = spacing[::-1]
            log.info(f"Creating thumbnails for image of shape {image.shape}")
            volume_dims = 3
            if mask is None and labels is not None:
                log.warning("Labels provided but no mask, setting labels to None")
                labels = None

            if mask is not None and labels is None:
                log.warning("Mask provided but no labels, setting mask to None")
                mask = None
            output = {}
            for axis in range(volume_dims):
                output[f"dim_{axis + 1}"] = self.create_img(
                    img_arr=image,
                    msk_arr=mask,
                    spacing=spacing,
                    labels=labels,
                    axis=axis,
                    opacity=opacity
                )
            log.success("=> Successfully created thumbnails")
            return output
        except ValueError as e:
            log.error(e)

    def hex_to_rgba(self, hex_string: str, alpha: float = 1.0) -> List[int]:
        """Converts a hex color string to an RGBA list.

        Parameters
        ----------
        hex_string : str
            The hex color string.
        alpha : float, optional
            The alpha value, by default 1.0.

        Returns
        -------
        list
            The RGBA list.
        """
        try:
            log.info("Converting hex string to RGBA")
            # Remove the "#" character from the beginning of the hex string
            hex_string = hex_string.lstrip("#")

            # Convert the hex string to integers for each color component
            red, green, blue = tuple(int(hex_string[color_component_index:color_component_index + 2], 16) for color_component_index in (0, 2, 4))

            # Create the RGBA list with the color components and alpha value
            rgba = [red, green, blue, alpha]
            log.success("=> Hex string converted to RGBA")
            return rgba
        except ValueError as e:
            log.error(f"Could not convert hex string to RGBA: {e}")
        except Exception as e:
            log.error(f"Unexpected error: {e}")

    def manage_save_cache(self) -> NoReturn:
        """Manages the cache of saved images."""
        log.info("Checking cache...")
        timezone = arrow.now().tzinfo
        critical_time = arrow.now().shift(seconds=-30)  # If 30 seconds have passed since the file was created, delete it
        os.makedirs(os.path.join(ROOT, 'temp'), exist_ok=True)
        for file in os.listdir(os.path.join(ROOT, 'temp')):
            file = os.path.join(ROOT, 'temp', file)
            if os.path.isfile(file):
                dt_file = os.path.getmtime(file)
                file_time = arrow.get(dt_file, tzinfo=timezone)
                if file_time < critical_time:
                    os.remove(file)
                    log.info(f"Cache file older than 30 seconds, deleting {file}")
        log.success("=> Cache checked")

    def orient_volume(self, image: np.ndarray, affine: np.ndarray) -> Tuple[np.ndarray, List[float]]:
        """Orients a volume to RPI.

        Parameters
        ----------
        image : np.ndarray
            The image array.
        affine : np.ndarray
            The affine array.

        Returns
        -------
        np.ndarray
            The oriented image array.
        
        """
        self.manage_save_cache()
        log.info("Orienting volume to LPI")
        tempfilename = os.path.join(ROOT, 'temp', str(uuid.uuid4()) + '.nii.gz')
        nifti = nib.Nifti1Image(image, affine)
        nib.save(nifti, tempfilename)
        simple_payload = sitk.ReadImage(tempfilename)
        # RPI, LPI, RAI, LAI, RPS, LPS, RAS, LAS
        data_payload_re = sitk.DICOMOrient(simple_payload, 'LPI')
        spacings = list(data_payload_re.GetSpacing()[::-1])
        data_payload_re = sitk.GetArrayFromImage(data_payload_re)
        log.success("=> Volume oriented to LPI")
        return data_payload_re, spacings

    def make_thumbnail_hex(self,
                           image: np.ndarray,
                           p_mask: np.ndarray,
                           affine: np.ndarray,
                           labels: Dict[str, str | int] = None,
                           format='jpeg') -> Dict[str, str]:
        """
        Make a thumbnail from a 3D image and mask.
        Parameters
        ----------
        image : np.ndarray
            The image array.
        p_mask : np.ndarray
            The mask array.
        affine : np.ndarray
            The affine array.
        labels : dict
            The labels of the image.
        format : str
            The format of the image.
        Returns
        -------
        Dict[str, str]
        """
        image_thumb = image.transpose(1, 0, 2)
        p_mask_thumb = p_mask.transpose(1, 0, 2)
        image_thumb, spacings = self.orient_volume(image=image_thumb,
                                                   affine=affine)
        p_mask_thumb, spacings = self.orient_volume(image=p_mask_thumb,
                                                    affine=affine)
        log.info(f'Got spacings for thumbnail: {spacings}')
        thumbnails_most_lesions = self.thumbnail_all_axis(image=image_thumb,
                                                          mask=p_mask_thumb,
                                                          spacing=spacings,
                                                          labels=labels
                                                          )
        img_mask_overlayed_hex = self.convert_all_axes_to_hex(imgs_dict=thumbnails_most_lesions,
                                                              format=format)
        log.success("=> Thumbnail created successfully")
        return img_mask_overlayed_hex
