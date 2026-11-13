<div class="langswitch langswitch-ltr">
  <strong>English</strong> · <a href="#lang-fa">فارسی</a>
</div>

# Exercise: Implementing Otsu's Thresholding from Scratch

## Introduction

In the clustering lecture, we introduced the **k-means** algorithm and its objective function. In this exercise, you will implement a classical application of the same idea in image processing: **Otsu's method** for finding an optimal threshold that separates foreground from background.

Otsu's method (Otsu, 1979) is an **unsupervised** technique that partitions pixel intensities into two groups so that the **within-class variance** is minimized. The goals of this exercise are:

1. Understand the mathematical foundation of Otsu's method.
2. See its connection to k-means.
3. Implement the method from scratch (without ready-made functions).
4. Evaluate the result on a real image.

---

## Part 1: Mathematical Background

### 1.1 Problem Setup

Let an image have $N$ pixels with intensities $x_1, x_2, \ldots, x_N \in \{0, 1, \ldots, L-1\}$ (typically $L = 256$). We want to find a threshold $t$ that splits the pixels into two groups:

$$
C_0(t) = \{x_i : x_i \le t\}, \qquad C_1(t) = \{x_i : x_i > t\}.
$$

Denote the means of the two groups by $\mu_0(t)$ and $\mu_1(t)$, their sizes by $n_0(t)$ and $n_1(t)$, and the overall mean by $\mu$.

### 1.2 Within-Class and Between-Class Variance

Two natural criteria for evaluating a threshold are:

**Within-class variance:**

$$
\sigma_W^2(t) = \frac{1}{N} \left( \sum_{x_i \in C_0(t)} (x_i - \mu_0(t))^2 + \sum_{x_i \in C_1(t)} (x_i - \mu_1(t))^2 \right)
$$

**Between-class variance:**

$$
\sigma_B^2(t) = \frac{n_0(t)}{N} (\mu_0(t) - \mu)^2 + \frac{n_1(t)}{N} (\mu_1(t) - \mu)^2
$$

Otsu's method selects the threshold that minimizes $\sigma_W^2(t)$ (equivalently, maximizes $\sigma_B^2(t)$):

$$
t^* = \arg\min_{t} \sigma_W^2(t) = \arg\max_{t} \sigma_B^2(t).
$$

### 1.3 Total-Variance Decomposition

**Lemma (Total-variance decomposition).** For any partition of the data into two groups $C_0$ and $C_1$,

$$
\sigma^2 = \sigma_W^2 + \sigma_B^2,
$$

where $\sigma^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2$ is the total variance of the data.

**Proof (sketch).** We use **Lemma 1** from the k-means lecture: for any group $C_c$ with mean $\mu_c$ and any reference point $z$,

$$
\sum_{x_i \in C_c} (x_i - z)^2 = \sum_{x_i \in C_c} (x_i - \mu_c)^2 + n_c (\mu_c - z)^2.
$$

Setting $z = \mu$, summing over the two groups, and dividing by $N$ yields the identity. $\blacksquare$

**Consequence.** Since $\sigma^2$ does not depend on $t$, maximizing $\sigma_B^2(t)$ is equivalent to minimizing $\sigma_W^2(t)$.

### 1.4 A Useful Reformulation of $\sigma_B^2$

For an efficient implementation, we use the following form:

$$
\sigma_B^2(t) = \frac{n_0(t) \, n_1(t)}{N^2} \left( \mu_0(t) - \mu_1(t) \right)^2.
$$

**Proof.** Substitute $\mu = \frac{n_0 \mu_0 + n_1 \mu_1}{N}$ and simplify. The form makes the intuition transparent: $\sigma_B^2$ is large when (i) the two group sizes are balanced ($n_0 \approx n_1$) and (ii) the group means are far apart.

### 1.5 Connection to k-means

The k-means objective for a two-group partition $\{C_0, C_1\}$ on 1D data is

$$
J = \sum_{x_i \in C_0} (x_i - \mu_0)^2 + \sum_{x_i \in C_1} (x_i - \mu_1)^2 = N \cdot \sigma_W^2.
$$

Thus, **minimizing the within-class variance is exactly minimizing the k-means objective on 1D data**. The key differences are:

- In k-means, the partition is searched iteratively and may converge to a local minimum.
- In Otsu's method, all $L$ candidate thresholds are evaluated exhaustively, so the **global optimum is guaranteed**.

> **Summary:** Otsu's method is a special case of k-means with $k = 2$ on 1D data, restricted to threshold-based partitions, and solved by exhaustive search rather than iterative refinement.

---

## Part 2: Algorithm

Otsu's method can be computed in $O(N + L)$ time using a histogram:

1. **Step 1 (histogram):** For each intensity level $v \in \{0, \ldots, L-1\}$, compute the number of pixels with intensity $v$: $h(v)$.
2. **Step 2 (cumulative sums):** For each $t$, compute:
   - $n_{\le}(t) = \sum_{v=0}^{t} h(v)$ (number of pixels with intensity $\le t$)
   - $S_{\le}(t) = \sum_{v=0}^{t} v \cdot h(v)$ (sum of intensities for pixels with intensity $\le t$)
   - and their complements: $n_{>}(t) = N - n_{\le}(t)$, $S_{>}(t) = S_{\text{total}} - S_{\le}(t)$
3. **Step 3 (evaluation):** For each $t$, compute the group means and then $\sigma_B^2(t)$.
4. **Step 4 (selection):** Return $t^* = \arg\max_t \sigma_B^2(t)$.

---

## Part 3: Practical Exercise

### 3.1 Requirements

Prepare a Jupyter notebook with the following components:

1. **Implement Otsu from scratch:** Write a function `otsu_threshold(image)` that returns the optimal threshold and the array of $\sigma_B^2(t)$ for all $t$. **Use of `skimage.filters.threshold_otsu` or any equivalent ready-made function is not allowed.**
2. **Implement segmentation:** Write a function `otsu_segment(image)` that builds a binary mask using the computed threshold.
3. **Sanity check:** Write a function that verifies the identity $\sigma^2 = \sigma_W^2 + \sigma_B^2$ for several random thresholds and reports the discrepancy.
4. **Comparison with a reference implementation:** Compare the result of your function with `skimage.filters.threshold_otsu` and confirm that the same threshold is obtained.
5. **Test on a real image:** Load a simple image (e.g., an object on a fairly uniform background) and perform the following:
   - Plot the input image, the intensity histogram, and the output mask in three panels side by side.
   - On the histogram, draw a vertical line at the Otsu threshold.
   - Plot $\sigma_B^2(t)$ versus $t$ and show that it attains its maximum at $t^*$.
6. **Observation report:** In a Markdown cell, answer the questions in Section 3.3.

### 3.2 Input Image

A sample image is provided alongside this exercise on the course page. You may use it or your own image (preferably with a fairly uniform background). If the image is color, convert it to grayscale first.

> **Important note:** Before any processing, check the data type and intensity range of the image using `print(image.dtype, image.min(), image.max())`. If the image is of type `float` in the range 0 to 1, multiply by 255 and convert it to `uint8` so that Otsu's method operates on integer levels.

### 3.3 Report Questions (answers required in the notebook)

1. What threshold did your implementation find? Is it the same as `skimage`'s? If not, why?
2. What is the shape of the $\sigma_B^2(t)$ curve? Does it have a single clear peak, or several? How do the peak(s) relate to the image histogram?
3. How well does the output mask match your expectation of foreground/background separation? Where do you observe errors?
4. In the sanity check (Item 3.1.3), what was the discrepancy between $\sigma^2$ and $\sigma_W^2 + \sigma_B^2$? Is it within floating-point rounding error?
5. (Optional) If you switch to an image with a busier background, how does the algorithm behave? Does Otsu still find a suitable threshold?

### 3.4 Starter Code (Skeleton)

Complete the following code in your notebook. **The overall structure must match this skeleton.**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
from skimage.filters import threshold_otsu


# ============================================================
# Part 1: Implement Otsu from scratch
# ============================================================

def otsu_threshold(image, n_levels=256):
    """
    Compute the Otsu threshold for a grayscale image.

    Parameters
    ----------
    image : np.ndarray
        Grayscale image with integer intensities in [0, n_levels - 1].
    n_levels : int
        Number of intensity levels (default 256).

    Returns
    -------
    t_star : int
        Optimal threshold.
    sigma_B2 : np.ndarray
        Between-class variance for each candidate threshold.
    """
    # Step 1: histogram
    hist = np.bincount(image.ravel(), minlength=n_levels).astype(float)
    N = hist.sum()
    if N == 0:
        raise ValueError("Empty image.")

    # Step 2: cumulative sums
    n_le = np.cumsum(hist)                            # n_<=(t)
    S_le = np.cumsum(hist * np.arange(n_levels))      # S_<=(t)
    S_total = S_le[-1]

    # Step 3: evaluate all thresholds
    sigma_B2 = np.zeros(n_levels - 1)
    for t in range(n_levels - 1):
        n0 = n_le[t]
        n1 = N - n0
        if n0 == 0 or n1 == 0:
            continue
        mu0 = S_le[t] / n0
        mu1 = (S_total - S_le[t]) / n1
        sigma_B2[t] = (n0 * n1 / N**2) * (mu0 - mu1) ** 2

    # Step 4: argmax
    t_star = int(np.argmax(sigma_B2))
    return t_star, sigma_B2


def otsu_segment(image, n_levels=256):
    """Return a binary mask using the Otsu threshold."""
    t_star, _ = otsu_threshold(image, n_levels)
    return (image > t_star).astype(np.uint8), t_star


# ============================================================
# Part 2: Sanity check of the total-variance decomposition
# ============================================================

def verify_total_variance_decomposition(x, t):
    """Verify sigma^2 = sigma_W^2 + sigma_B^2 for a 1D dataset and threshold."""
    x = np.asarray(x, dtype=float)
    N = len(x)
    mu = x.mean()
    sigma2 = ((x - mu) ** 2).mean()

    C0 = x[x <= t]
    C1 = x[x > t]
    mu0, mu1 = C0.mean(), C1.mean()
    sigma_W2 = (((C0 - mu0) ** 2).sum() + ((C1 - mu1) ** 2).sum()) / N
    sigma_B2 = (len(C0) / N) * (mu0 - mu) ** 2 + (len(C1) / N) * (mu1 - mu) ** 2

    return sigma2, sigma_W2 + sigma_B2


# ============================================================
# Part 3: Load the image and compare
# ============================================================

# TODO: load the image and convert it to grayscale
# img = io.imread('sample.png')
# if img.ndim == 3:
#     img = (color.rgb2gray(img) * 255).astype(np.uint8)
# print(img.dtype, img.min(), img.max())

# TODO: threshold with your implementation
# t_mine, sigma_B2 = otsu_threshold(img)

# TODO: threshold with skimage
# t_skimage = threshold_otsu(img)

# print(f"My threshold:      {t_mine}")
# print(f"skimage threshold: {t_skimage}")

# TODO: build the binary mask
# mask, t_star = otsu_segment(img)

# TODO: three-panel visualization
# (input image, histogram with threshold, output mask)

# TODO: plot sigma_B2(t) versus t
```
