"""
Advanced Change Detection Module
Uses Structural Similarity (SSIM) for robust change detection
"""

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from typing import Tuple
from PIL import Image, ImageDraw

def advanced_change_detection(image_path_t0: str, image_path_t1: str):
    """
    Performs an advanced change detection using Structural Similarity (SSIM).
    This is much more robust than simple pixel difference.
    
    In a V3 system, you would replace this function with inference
    from a trained Siamese UNet++ model from a library like
    segmentation-models-pytorch (smp).
    
    Returns:
        tuple: (binary_change_mask, ssim_score)
    """
    try:
        img_t0 = cv2.imread(image_path_t0)
        img_t1 = cv2.imread(image_path_t1)
        
        if img_t0 is None or img_t1 is None:
            raise FileNotFoundError("One or both images not found.")

        # Resize for consistent comparison (optional, but good practice)
        img_t1 = cv2.resize(img_t1, (img_t0.shape[1], img_t0.shape[0]))

        # Convert to grayscale for SSIM
        gray_t0 = cv2.cvtColor(img_t0, cv2.COLOR_BGR2GRAY)
        gray_t1 = cv2.cvtColor(img_t1, cv2.COLOR_BGR2GRAY)

        # --- Calculate Structural Similarity (SSIM) ---
        # 'score' is the overall similarity (1.0 = identical)
        # 'diff' is an image highlighting the differences
        (score, diff) = ssim(gray_t0, gray_t1, full=True)
        diff = (diff * 255).astype("uint8")
        
        print(f"[ChangeDetection] Structural Similarity Score (SSIM): {score:.4f}")

        # --- Create Binary Mask ---
        # 1. Threshold the difference image
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # 2. Clean up noise using morphology
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        # 3. Find contours (blobs) of change
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        final_mask = np.zeros_like(gray_t0)
        
        for c in contours:
            # --- Filter out tiny, insignificant changes ---
            if cv2.contourArea(c) > 100:  # Only draw changes > 100 pixels
                cv2.drawContours(final_mask, [c], -1, 255, -1)  # Fill contour

        print(f"[ChangeDetection] Generated mask with {len(contours)} contours.")
        # The final_mask is a clean, binary image of *significant* changes
        return final_mask, score

    except Exception as e:
        print(f"[Error] Advanced change detection failed: {e}")
        return np.zeros((512, 512), dtype=np.uint8), 1.0


def detect_changes(image_path_t0: str, image_path_t1: str) -> np.ndarray:
    """
    Legacy change detection function - kept for backwards compatibility
    """
    try:
        img_t0 = cv2.imread(image_path_t0, cv2.IMREAD_GRAYSCALE)
        img_t1 = cv2.imread(image_path_t1, cv2.IMREAD_GRAYSCALE)
        
        if img_t0 is None or img_t1 is None:
            raise FileNotFoundError("One or both images not found.")

        # Placeholder logic for demonstration:
        diff = cv2.absdiff(img_t0, img_t1)
        
        # Apply a threshold to get a binary mask
        _, change_mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        # Noise reduction (optional but good)
        change_mask = cv2.morphologyEx(change_mask, cv2.MORPH_OPEN, kernel=np.ones((3,3),np.uint8))
        
        print(f"[ChangeDetection] Successfully generated change mask.")
        return change_mask

    except Exception as e:
        print(f"[Error] Change detection failed: {e}")
        return np.zeros((512, 512), dtype=np.uint8)  # Return empty mask

if __name__ == "__main__":
    # Create dummy images for testing
    img_before = Image.new('RGB', (512, 512), color = 'gray')
    img_before.save("dummy_before.png")
    
    img_after = Image.new('RGB', (512, 512), color = 'gray')
    # Draw a "new" rectangle
    draw = ImageDraw.Draw(img_after)
    draw.rectangle([100, 100, 200, 200], fill='white')
    img_after.save("dummy_after.png")
    
    mask = detect_changes("dummy_before.png", "dummy_after.png")
    cv2.imwrite("change_mask.png", mask)
    print("Change mask saved to change_mask.png")
