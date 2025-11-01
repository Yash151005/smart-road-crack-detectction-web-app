import cv2
import numpy as np
import os

def detect_cracks(input_path, output_path):
    """
    Detect road cracks using robust image processing (no ML).
    Produces overlay image and binary mask.
    """
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {input_path}")

    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Noise reduction (bilateral filter keeps edges)
    denoised = cv2.bilateralFilter(gray, 9, 75, 75)

    # 3. Contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)

    # 4. Edge/Crack extraction
    # Top-hat morphology to extract bright thin cracks
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    tophat = cv2.morphologyEx(enhanced, cv2.MORPH_TOPHAT, kernel)

    # Laplacian + Sobel to detect edges
    laplacian = cv2.Laplacian(tophat, cv2.CV_8U)
    sobelx = cv2.Sobel(tophat, cv2.CV_8U, 1, 0, ksize=3)
    sobely = cv2.Sobel(tophat, cv2.CV_8U, 0, 1, ksize=3)
    edges = cv2.bitwise_or(laplacian, cv2.bitwise_or(sobelx, sobely))

    # 5. Threshold to binary mask
    _, mask = cv2.threshold(edges, 30, 255, cv2.THRESH_BINARY)

    # 6. Morphological cleaning
    morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, morph_kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, morph_kernel, iterations=1)

    # 7. Overlay cracks in red
    overlay = img.copy()
    overlay[mask > 0] = [0, 0, 255]

    # Save results
    cv2.imwrite(output_path, overlay)
    mask_path = os.path.splitext(output_path)[0] + "_mask.png"
    cv2.imwrite(mask_path, mask)

    return mask_path

def calculate_crack_percentage(mask_path):
    """
    Calculate % of pixels marked as cracks.
    """
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise FileNotFoundError(f"Mask not found: {mask_path}")

    total_pixels = mask.size
    crack_pixels = cv2.countNonZero(mask)
    percentage = (crack_pixels / total_pixels) * 100
    return round(percentage, 2)
