
def mohsen1(
    path: PathType,
    method: str,
    voxel_size=[1, 1, 1],
    save=True,
    save_path=None,
    out_name: str = None,
) -> sitk.Image:
    path = path_in(path)

    if method == "trilinear":
        interpolator = sitk.sitkLinear
    elif method == "nearest":
        interpolator = sitk.sitkNearestNeighbor
    else:
        raise ValueError("Unknown interpolation method")

    image = sitk.ReadImage(path)

    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputSpacing(voxel_size)

    print(f"Original spacing: {image.GetSpacing()}")
    print(f"Original size: {image.GetSize()}")

    # resampler.SetSize(
    #     [
    #         int(sz / vx * voxel_size[1])
    #         for sz, vx in zip(image.GetSize(), image.GetSpacing())
    #     ]
    # )

    # resampler.SetOutputDirection(image.GetDirection())
    # resampler.SetOutputOrigin(image.GetOrigin())
    # resampler.SetInterpolator(interpolator)

    # resampler.SetSize(
    #     [
    #         int(sz / vx * nv)
    #         for sz, vx, nv in zip(image.GetSize(), image.GetSpacing(), voxel_size)
    #     ]
    # )

    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputSpacing(voxel_size)
    resampler.SetOutputDirection(image.GetDirection())
    resampler.SetOutputOrigin(image.GetOrigin())
    resampler.SetInterpolator(interpolator)
    resampler.SetSize(
        [
            int(sz / vx * nv)
            for sz, vx, nv in zip(image.GetSize(), image.GetSpacing(), voxel_size)
        ]
    )

    resampled_image = resampler.Execute(image)

    print(f"New spacing: {resampled_image.GetSpacing()}")
    print(f"New size: {resampled_image.GetSize()}")


# def mohsen(
#     path: PathType,
#     method: str,
#     voxel_size=[1, 1, 1],
#     save=True,
#     save_path=None,
#     out_name: str = None,
# ) -> sitk.Image:
#     path = path_in(path)

#     if method == "trilinear":
#         interpolator = sitk.sitkLinear
#     elif method == "nearest":
#         interpolator = sitk.sitkNearestNeighbor
#     else:
#         raise ValueError("Unknown interpolation method")

#     image = sitk.ReadImage(path)

#     # Explicitly calculate new sizes
#     new_sizes = [
#         int(old_size * (old_spacing / new_spacing))
#         for old_size, old_spacing, new_spacing in zip(image.GetSize(), image.GetSpacing(), voxel_size)
#     ]

#     resampler = sitk.ResampleImageFilter()
#     resampler.SetOutputSpacing(voxel_size)
#     resampler.SetOutputDirection(image.GetDirection())
#     resampler.SetOutputOrigin(image.GetOrigin())
#     resampler.SetInterpolator(interpolator)
#     resampler.SetSize(new_sizes)  # Set sizes explicitly

#     resampled_image = resampler.Execute(image)

#     print(f"Original spacing: {image.GetSpacing()}")
#     print(f"Original size: {image.GetSize()}")
#     print(f"New spacing: {resampled_image.GetSpacing()}")
#     print(f"New size: {resampled_image.GetSize()}")

#     if save:
#         suffix = path.suffix

#         if not save_path:
#             save_path = path.parent

#         if not out_name:
#             stem = path.stem
#             out_name = f"{stem}_isotropic{suffix}"

#             out_path = Path(save_path) / out_name

#             full_path = save_path_file(out_path, suffix)

#             sitk.WriteImage(resampled_image, str(full_path))
#             print(f"Saved to {full_path}")

#     return resampled_image
