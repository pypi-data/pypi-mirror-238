
def reader(path: PathMedicalImage) -> PathMedicalImage:
    """
    Read the medical image based on its file extension.

    This function supports various medical image file formats, including
    but not limited to NIfTI (`.nii`, `.nii.gz`), DICOM (`.dcm`), MHA (`.mha`),
    and NumPy arrays (`.npy`, `.npz`).

    Parameters:
        path (PathMedicalImage): Path to the medical image file or an already loaded image object.
                                 Expected types include str, Path, or specific medical image objects
                                 like MedicalImage.

    Returns:
        object: Loaded medical image object.

    Raises:
        TypeError: If the provided file format is unsupported.
    """
    if isinstance(path, MedicalImage):
        return path

    path = path_in(path)
    if path.suffix in [".nii", ".nii.gz"]:
        return nib.load(path)
    elif path.suffix == ".dcm":
        return dicom.dcmread(path)
    elif path.suffix == ".mha":
        return sitk.ReadImage(str(path))
    elif path.suffix == ".npy":
        return np.load(path)
    elif path.suffix == ".npz":
        return np.load(path)["arr_0"]
    else:
        raise TypeError(f"Unsupported file type: {path.suffix}")


def reader(*paths: Union[str, Path]) -> Union[object, Tuple[object]]:
    """
    Read one or more medical images based on their file extensions.

    This function supports various medical image file formats, including
    but not limited to NIfTI (`.nii`, `.nii.gz`), DICOM (`.dcm`), MHA (`.mha`),
    and NumPy arrays (`.npy`, `.npz`).

    Parameters:
        *paths (Union[str, Path]): Paths to the medical image files or already loaded image objects.

    Returns:
        Union[object, Tuple[object]]: If a single path is provided, returns a single loaded medical image object.
                                      If multiple paths are provided, returns a tuple of loaded medical image objects.

    Raises:
        TypeError: If the provided file format is unsupported.
    """

    def load_image(path: Union[str, Path]) -> object:
        if isinstance(path, MedicalImage):
            return path

        path_obj = path_in(path)

        if path_obj.suffix in [".nii", ".nii.gz"]:
            return nib.load(path_obj)
        elif path_obj.suffix == ".dcm":
            return dicom.dcmread(path_obj)
        elif path_obj.suffix == ".mha":
            return sitk.ReadImage(str(path_obj))
        elif path_obj.suffix == ".npy":
            return np.load(path_obj)
        elif path_obj.suffix == ".npz":
            return np.load(path_obj)["arr_0"]
        else:
            raise TypeError(f"Unsupported file type: {path_obj.suffix}")

    images = tuple(load_image(path) for path in paths)
    if len(images) == 1:
        return images[0]
    return images