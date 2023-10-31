from anyscale.shared_anyscale_utils.utils.ray_semver import ray_semver_compare


def get_alias_for_base_image_name(base_image_name: str) -> str:
    """
    Modify a base image name to comply with Ray version and naming conventions.

    This function takes a base image name as input, extracts the Ray version, and checks if the version
    is greater than or equal to '2.7.0', or falls back to the original name.

    Args:
        base_image_name (str): The name of the base image to be checked.

    Returns:
        str: The modified base image name based on version and naming conventions.

    Example:
        To check a base image name, you can call this function like this:
        >>> get_alias_for_base_image_name("anyscale/ray:2.7.0-py38-cuda121"), it should be modified to "anyscale/ray:2.7.0oss-py38-cuda121"
    """
    # to extract "2.7.0", "2.7.0oss", "2.7.0optimized", "2.0.1rc" as ray_version
    ray_version = get_ray_version(base_image_name)

    if ray_version.endswith(("optimized", "oss")) or "rc" in ray_version:
        return base_image_name

    if ray_semver_compare(ray_version, "2.7.0") >= 0:  # ray_version >= "2.7.0"
        return base_image_name.replace(ray_version, f"{ray_version}optimized")
    return base_image_name


def get_ray_version(base_image: str) -> str:
    """Returns the Ray version in use based on the base image.

    Args:
        base_image: e.g. anyscale/ray-ml:1.9.0-cpu

    Returns:
        The ray version, e.g. 1.9.0.
    """
    # e.g. 1.9.0-cpu
    image_version = base_image.split(":")[-1]
    # e.g. 1.9.0
    ray_version = image_version.split("-")[0]
    return ray_version
