<div class="langswitch">
  <a href="#lang-en">English</a> · <strong>فارسی</strong>
</div>

# تمرین: پیاده‌سازی آستانه‌گذاری اوتسو از صفر

## مقدمه

در درس خوشه‌بندی، الگوریتم **k-means** و تابع هدفش را معرفی کردیم. در این تمرین، کاربرد کلاسیکی از
همان ایده در پردازش تصویر را پیاده می‌کنید: **روش اوتسو** برای یافتن آستانه‌ای بهینه که پیش‌زمینه را
از پس‌زمینه جدا کند.

روش اوتسو (Otsu, 1979) تکنیکی **بدون‌نظارت** است که شدت پیکسل‌ها را به دو گروه افراز می‌کند تا
**واریانس درون‌کلاسی** کمینه شود. هدف‌های این تمرین:

1. فهم بنیاد ریاضی روش اوتسو.
2. دیدن پیوندش با k-means.
3. پیاده‌سازی روش از صفر (بدون توابع آماده).
4. ارزیابی نتیجه روی یک تصویر واقعی.

---

## بخش ۱: پیشینهٔ ریاضی

### ۱.۱ صورت‌بندی مسئله

تصویری با $N$ پیکسل و شدت‌های $x_1, x_2, \ldots, x_N \in \{0, 1, \ldots, L-1\}$ داشته باشید (معمولاً
$L = 256$). می‌خواهیم آستانهٔ $t$ را بیابیم که پیکسل‌ها را به دو گروه بشکند:

$$
C_0(t) = \{x_i : x_i \le t\}, \qquad C_1(t) = \{x_i : x_i > t\}.
$$

میانگین دو گروه را $\mu_0(t)$ و $\mu_1(t)$، اندازه‌شان را $n_0(t)$ و $n_1(t)$ و میانگین کل را $\mu$
بنامید.

### ۱.۲ واریانس درون‌کلاسی و میان‌کلاسی

دو معیار طبیعی برای ارزیابی یک آستانه:

**واریانس درون‌کلاسی:**

$$
\sigma_W^2(t) = \frac{1}{N} \left( \sum_{x_i \in C_0(t)} (x_i - \mu_0(t))^2 + \sum_{x_i \in C_1(t)} (x_i - \mu_1(t))^2 \right)
$$

**واریانس میان‌کلاسی:**

$$
\sigma_B^2(t) = \frac{n_0(t)}{N} (\mu_0(t) - \mu)^2 + \frac{n_1(t)}{N} (\mu_1(t) - \mu)^2
$$

روش اوتسو آستانه‌ای را برمی‌گزیند که $\sigma_W^2(t)$ را کمینه می‌کند (به‌طور معادل، $\sigma_B^2(t)$ را
بیشینه می‌کند):

$$
t^* = \arg\min_{t} \sigma_W^2(t) = \arg\max_{t} \sigma_B^2(t).
$$

### ۱.۳ تجزیهٔ واریانس کل

**لم (تجزیهٔ واریانس کل).** برای هر افراز داده به دو گروه $C_0$ و $C_1$،

$$
\sigma^2 = \sigma_W^2 + \sigma_B^2,
$$

که در آن $\sigma^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2$ واریانس کل داده است.

**اثبات (طرح).** از **لم ۱** درس k-means بهره می‌بریم: برای هر گروه $C_c$ با میانگین $\mu_c$ و هر نقطهٔ
مرجع $z$،

$$
\sum_{x_i \in C_c} (x_i - z)^2 = \sum_{x_i \in C_c} (x_i - \mu_c)^2 + n_c (\mu_c - z)^2.
$$

با گذاشتن $z = \mu$، جمع روی دو گروه و تقسیم بر $N$، اتحاد به دست می‌آید. $\blacksquare$

**نتیجه.** چون $\sigma^2$ به $t$ وابسته نیست، بیشینه‌کردن $\sigma_B^2(t)$ معادل کمینه‌کردن
$\sigma_W^2(t)$ است.

### ۱.۴ صورت‌بندی سودمند دیگری از $\sigma_B^2$

برای پیاده‌سازی کارا از این شکل بهره می‌بریم:

$$
\sigma_B^2(t) = \frac{n_0(t) \, n_1(t)}{N^2} \left( \mu_0(t) - \mu_1(t) \right)^2.
$$

**اثبات.** $\mu = \frac{n_0 \mu_0 + n_1 \mu_1}{N}$ را جای‌گذاری و ساده کنید. این شکل شهود را شفاف
می‌کند: $\sigma_B^2$ وقتی بزرگ است که (الف) اندازهٔ دو گروه متوازن باشد ($n_0 \approx n_1$) و (ب)
میانگین‌های دو گروه از هم دور باشند.

### ۱.۵ پیوند با k-means

تابع هدف k-means برای افراز دوگروهی $\{C_0, C_1\}$ روی دادهٔ یک‌بُعدی چنین است:

$$
J = \sum_{x_i \in C_0} (x_i - \mu_0)^2 + \sum_{x_i \in C_1} (x_i - \mu_1)^2 = N \cdot \sigma_W^2.
$$

پس **کمینه‌کردن واریانس درون‌کلاسی دقیقاً همان کمینه‌کردن تابع هدف k-means روی دادهٔ یک‌بُعدی است**.
تفاوت‌های کلیدی:

- در k-means افراز به‌صورت تکراری جست‌وجو می‌شود و ممکن است به کمینهٔ محلی برسد.
- در روش اوتسو هر $L$ آستانهٔ نامزد برای‌بررسی شمرده می‌شود، پس **بهینهٔ جهانی تضمین‌شده** است.

> **خلاصه:** روش اوتسو حالت خاص k-means با $k = 2$ روی دادهٔ یک‌بُعدی است، محدود به افرازهای
> آستانه‌بنیان، و با جست‌وجوی فراگیر حل می‌شود نه با پالایش تکراری.

---

## بخش ۲: الگوریتم

روش اوتسو را می‌توان با هیستوگرام در زمان $O(N + L)$ حساب کرد:

1. **گام ۱ (هیستوگرام):** برای هر سطح شدت $v \in \{0, \ldots, L-1\}$ تعداد پیکسل‌های با شدت $v$ را
   حساب کنید: $h(v)$.
2. **گام ۲ (جمع‌های تجمعی):** برای هر $t$ حساب کنید:
   - $n_{\le}(t) = \sum_{v=0}^{t} h(v)$ (تعداد پیکسل‌های با شدت $\le t$)
   - $S_{\le}(t) = \sum_{v=0}^{t} v \cdot h(v)$ (جمع شدت‌های پیکسل‌های با شدت $\le t$)
   - و متمم‌هایشان: $n_{>}(t) = N - n_{\le}(t)$، $S_{>}(t) = S_{\text{total}} - S_{\le}(t)$
3. **گام ۳ (ارزیابی):** برای هر $t$ میانگین گروه‌ها و سپس $\sigma_B^2(t)$ را حساب کنید.
4. **گام ۴ (انتخاب):** $t^* = \arg\max_t \sigma_B^2(t)$ را برگردانید.

---

## بخش ۳: تمرین عملی

### ۳.۱ خواسته‌ها

نوت‌بوکی جوبایتر با این اجزا آماده کنید:

1. **پیاده‌سازی اوتسو از صفر:** تابعی به نام `otsu_threshold(image)` بنویسید که آستانهٔ بهینه و آرایهٔ
   $\sigma_B^2(t)$ را برای همهٔ $t$ برگرداند. **استفاده از `skimage.filters.threshold_otsu` یا هر
   تابع آمادهٔ معادل مجاز نیست.**
2. **پیاده‌سازی قطعه‌بندی:** تابعی به نام `otsu_segment(image)` بنویسید که با آستانهٔ محاسبه‌شده یک
   ماسک دودویی بسازد.
3. **بررسی درستی:** تابعی بنویسید که اتحاد $\sigma^2 = \sigma_W^2 + \sigma_B^2$ را برای چند آستانهٔ
   تصادفی بررسی کند و اختلاف را گزارش دهد.
4. **مقایسه با پیاده‌سازی مرجع:** نتیجهٔ تابع خود را با `skimage.filters.threshold_otsu` مقایسه کنید و
   تأیید کنید که همان آستانه به دست می‌آید.
5. **آزمون روی تصویر واقعی:** تصویری ساده بارگذاری کنید (مثلاً یک شیء روی پس‌زمینهٔ نسبتاً یکنواخت) و
   این کارها را انجام دهید:
   - تصویر ورودی، هیستوگرام شدت و ماسک خروجی را در سه پنل کنار هم رسم کنید.
   - روی هیستوگرام، خط عمودی در آستانهٔ اوتسو بکشید.
   - $\sigma_B^2(t)$ را برحسب $t$ رسم کنید و نشان دهید بیشینه‌اش در $t^*$ است.
6. **گزارش مشاهدات:** در یک سلول Markdown به پرسش‌های بخش ۳.۳ پاسخ دهید.

### ۳.۲ تصویر ورودی

تصویری نمونه در کنار همین تمرین در صفحهٔ درس آمده است. می‌توانید آن یا تصویر خودتان را به کار ببرید
(ترجیحاً با پس‌زمینهٔ نسبتاً یکنواخت). اگر تصویر رنگی است، نخست آن را به خاکستری تبدیل کنید.

> **نکتهٔ مهم:** پیش از هر پردازشی، نوع داده و بازهٔ شدت تصویر را با
> `print(image.dtype, image.min(), image.max())` بررسی کنید. اگر تصویر از نوع `float` در بازهٔ ۰ تا ۱
> است، آن را در ۲۵۵ ضرب و به `uint8` تبدیل کنید تا روش اوتسو روی سطح‌های صحیح کار کند.

### ۳.۳ پرسش‌های گزارش (پاسخ در نوت‌بوک لازم است)

1. پیاده‌سازی شما چه آستانه‌ای یافت؟ با آستانهٔ `skimage` یکسان است؟ اگر نه، چرا؟
2. شکل منحنی $\sigma_B^2(t)$ چگونه است؟ یک قلهٔ روشن دارد یا چند؟ قله(ها) با هیستوگرام تصویر چه
   نسبتی دارند؟
3. ماسک خروجی چقدر با انتظار شما از جدایی پیش‌زمینه/پس‌زمینه می‌خواند؟ کجا خطا می‌بینید؟
4. در بررسی درستی (بند ۳.۱.۳)، اختلاف میان $\sigma^2$ و $\sigma_W^2 + \sigma_B^2$ چقدر بود؟ در حد
   خطای گردکردن ممیز شناور است؟
5. (اختیاری) اگر به تصویری با پس‌زمینهٔ شلوغ‌تر بروید، الگوریتم چگونه رفتار می‌کند؟ آیا اوتسو هنوز
   آستانهٔ مناسبی می‌یابد؟

### ۳.۴ کد آغازین (اسکلت)

کد زیر را در نوت‌بوک خود کامل کنید. **ساختار کلی باید با این اسکلت بخواند.**

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

