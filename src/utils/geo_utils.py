import rasterio
from rasterio.transform import Affine

def convert_pixels_to_geojson(pixel_data: list, aoi_bounds: dict, image_dims: tuple):
    """
    Converts a list of pixel-based detections into a GeoJSON FeatureCollection.
    
    Args:
        pixel_data (list): List of detection dicts, e.g.,
                           [{"bbox_pixels": [x1, y1, x2, y2], ...}]
        aoi_bounds (dict): The Lat/Lng bounds from the frontend, e.g.,
                           {"north_east": {"lat": y, "lng": x}, "south_west": ...}
        image_dims (tuple): The (height, width) of the image processed.
    """
    
    img_height, img_width = image_dims
    
    # Get the corners from the AOI
    min_lng = aoi_bounds["south_west"]["lng"]
    min_lat = aoi_bounds["south_west"]["lat"]
    max_lng = aoi_bounds["north_east"]["lng"]
    max_lat = aoi_bounds["north_east"]["lat"]
    
    # Calculate the total geographic span
    span_lng = max_lng - min_lng
    span_lat = max_lat - min_lat
    
    def pixel_to_geo(px, py):
        """
        Maps a single (x, y) pixel coordinate to a (lng, lat) coordinate.
        """
        # Calculate percentage of pixel across the image
        percent_x = px / img_width
        percent_y = py / img_height
        
        # Apply that percentage to the geographic span
        # Note: Latitude (Y) is inverted. 0px is max_lat, img_height is min_lat.
        lng = min_lng + (percent_x * span_lng)
        lat = max_lat - (percent_y * span_lat)
        
        return [lng, lat]

    features = []
    for item in pixel_data:
        if "bbox_pixels" not in item:
            continue
            
        x1, y1, x2, y2 = item["bbox_pixels"]
        
        # Get center of the box
        center_x_pixel = (x1 + x2) / 2
        center_y_pixel = (y1 + y2) / 2
        
        # Convert center pixel to geo coordinate
        [lng, lat] = pixel_to_geo(center_x_pixel, center_y_pixel)
        
        # Create a GeoJSON Feature
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat]  # GeoJSON is [Lng, Lat]
            },
            "properties": {
                "type": item.get("type", "Unknown"),
                "class": item.get("class", "Unknown"),
                "confidence": item.get("confidence", 0.0)
            }
        }
        features.append(feature)

    # Wrap all features in a FeatureCollection
    return {
        "type": "FeatureCollection",
        "features": features
    }


def convert_to_geojson(fused_data, image_bounds_latlng):
    """
    Converts pixel-based fused data to a GeoJSON FeatureCollection.

    In a REAL system, you'd use rasterio to read the GeoTIFF transform.
    For SIH, we can *simulate* this by creating a simple
    linear transformation from the known image_bounds.
    """

    # Mocking the bounds and image size for the demo
    # (min_lat, min_lng), (max_lat, max_lng)
    (min_lat, min_lng) = image_bounds_latlng[0]
    (max_lat, max_lng) = image_bounds_latlng[1]

    # Assume a 1024x1024 image
    img_width_pixels = 1024
    img_height_pixels = 1024

    # Calculate how much lat/lng each pixel represents
    pixel_width_geo = (max_lng - min_lng) / img_width_pixels
    pixel_height_geo = (max_lat - min_lat) / img_height_pixels

    def pixel_to_geo(px, py):
        """Simple linear interpolation"""
        lng = min_lng + (px * pixel_width_geo)
        lat = max_lat - (py * pixel_height_geo) # Y is inverted
        return [lng, lat]

    features = []
    for item in fused_data:
        if "bbox_pixels" in item:
            x1, y1, x2, y2 = item["bbox_pixels"]

            # Get center of the box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            # Convert center pixel to geo coordinate
            [lng, lat] = pixel_to_geo(center_x, center_y)

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat] # GeoJSON is [lng, lat]
                },
                "properties": {
                    "type": item.get("type"),
                    "class": item.get("class"),
                    "details": str(item)
                }
            }
            features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }
