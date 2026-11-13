# دوزبانه کردن مطالب سایت — راهنمای کلی

این فایل دستور کارِ عامل هوشمند (یا انسان) است برای ترجمهٔ بقیهٔ مطالب. قاعده‌ها را
عوض نکنید مگر اینکه شکستنشان را با build آزمایش کرده باشید.

## ۱. قاعدهٔ اصلی

مخزن **دو پروژهٔ MyST** دارد، نه دو مخزن:

| مسیر | چیست |
| --- | --- |
| `myst.yml` + `notebooks/` | نسخهٔ انگلیسی؛ مرجع و منبع حقیقت (canonical) |
| `fa/myst.yml` + `fa/` | نسخهٔ فارسی؛ همان ساختار پوشه و **همان نام فایل** |
| `css/fa.css` | RTL برای فارسی؛ کد، فرمول و جدول را به LTR برمی‌گرداند |
| `tools/build_sites.py` | هر دو را می‌سازد، فارسی را در `_build/html/fa` می‌گذارد، سوییچ را وصل می‌کند |

مثلاً `notebooks/high-dimensional-spaces/Clustering-Part2.ipynb` ترجمه‌اش می‌شود
`fa/high-dimensional-spaces/Clustering-Part2.ipynb`. **نام فایل و جای آن در درخت
پوشه‌ها هرگز ترجمه نمی‌شود**؛ همین تقارن است که سوییچ زبان و لینک‌های نسبی را
قابل محاسبه می‌کند.

## ۲. گام‌به‌گام برای یک صفحهٔ `.md`

1. متن انگلیسی را کامل بخوانید (نه فقط عنوان).
2. فایل فارسی را در همان مسیر زیر `fa/` بسازید و متن را ترجمه کنید.
3. این بلوک را **اولین** چیزی در فایل بگذارید (برای وصل شدن به نسخهٔ انگلیسی):

   ```html
   <div class="langswitch">
     <a href="#lang-en">English</a> · <strong>فارسی</strong>
   </div>
   ```

   `href="#lang-en"` جای‌نگهدار است؛ `tools/build_sites.py` بعد از build آن را به
   مسیر نسبی درست به نسخهٔ انگلیسی همان صفحه تبدیل می‌کند.
4. تصاویر: هر مسیری که در متن انگلیسی هست (`img/...`، `../img/...`) باید **در
   درخت `fa/` هم وجود داشته باشد**؛ فایل را کپی کنید (پروژهٔ فارسی به بیرون از
   `fa/` دسترسی مسیر ندارد). مسیر را در متن دست نزنید.
5. در `fa/myst.yml` مدخل صفحه را از بلوک کامنت‌شدهٔ پایین به فهرست واقعی منتقل
   کنید. تا صفحه‌ای وجود ندارد، مدخلش را از کامنت درنیاورید (build می‌شکند).

## ۳. گام‌به‌گام برای یک نوتبوک `.ipynb`

قاعده: **فقط سلول‌های `markdown` ترجمه می‌شوند**. سلول‌های `code` با خروجی‌ها و
`execution_count` دست‌نخورده کپی می‌شوند تا دو نسخه هرگز در نتایج واگرا نشوند و
لازم نباشد چیزی اجرا شود.

اسکریپت آماده (همین کار را برای Clustering-Part2 کرده است):

```python
import pathlib, nbformat

SRC = pathlib.Path("notebooks/PATH/Page.ipynb")
DST = pathlib.Path("fa/PATH/Page.ipynb")
FA = {0: "...", 3: "...", 7: "..."}   # شمارهٔ سلول -> متن فارسی

nb = nbformat.read(SRC, as_version=4)
for i, text in FA.items():
    assert nb.cells[i].cell_type == "markdown", i
    nb.cells[i].source = text
missing = [i for i, c in enumerate(nb.cells)
           if c.cell_type == "markdown" and i not in FA]
assert not missing, f"سلول ترجمه‌نشده: {missing}"
DST.parent.mkdir(parents=True, exist_ok=True)
nbformat.write(nb, DST)
```

قبل از ترجمه، فهرست سلول‌ها را ببینید:

```python
import nbformat
nb = nbformat.read("notebooks/PATH/Page.ipynb", as_version=4)
for i, c in enumerate(nb.cells):
    print(i, c.cell_type, "".join(c["source"])[:70].replace("\n", " "))
```

شمارهٔ سلول‌ها را از خروجی همین حلقه بردارید (شماره‌گذاری از صفر است و شامل
سلول‌های کد هم می‌شود). بلوک سوییچ را به سلول صفرِ **هر دو** نسخه اضافه کنید:
در نسخهٔ فارسی `<div class="langswitch">` با `#lang-en`، و در نسخهٔ انگلیسی
`<div class="langswitch langswitch-ltr">` با `#lang-fa` (کلاس `-ltr` چون آن صفحه
چپ‌به‌راست است).

## ۴. چیزهایی که ترجمه نمی‌شوند

- کد، نام متغیرها، نام کلاس‌ها و توابع، کامنت‌های داخل کد (اختیاری، ولی بهتر است
  دست نخورد)، خروجی‌ها.
- فرمول‌های `$...$` و `$$...$$`، `\ref`/`\label`، `{numref}`، شناسه‌های
  headingها و `{figure}`/`{table}` ها.
- مسیر فایل‌ها، لینک‌های بیرونی، `title:` در `myst.yml` صفحه‌ها، نام فایل.
- ارجاع به صفحات دیگر سایت: لینک‌ها در فارسی باید **به صفحهٔ فارسی** اشاره کنند
  (`[ماتریس](../linear-algebra/linear-algebra-basics.md)` نه به نسخهٔ انگلیسی).

## ۵. اصطلاح‌نامه (یکدست بمانید)

| English | فارسی |
| --- | --- |
| data point / sample | نقطهٔ داده / نمونه |
| feature / dimension | ویژگی / بُعد |
| clustering | خوشه‌بندی |
| cluster | خوشه |
| centroid | مرکز (سنتروئید) |
| partition | افراز |
| representative-based | نماینده‌بنیان |
| classification | دسته‌بندی |
| label | برچسب |
| training / test set | مجموعهٔ آموزش / آزمون |
| overfitting | بیش‌برازش |
| underfitting | کم‌برازش |
| loss / cost function | تابع هزینه |
| gradient descent | گرادیان کاهشی |
| eigenvector / eigenvalue | بردار ویژه / مقدار ویژه |
| singular value | مقدار تکین |
| rank | رتبه |
| subspace | زیرفضا |
| projection | تصویر (تصویرسازی) |
| random graph | گراف تصادفی |
| degree | درجه |
| phase transition | گذار فازی |
| exercise | تمرین |
| hypersphere / hyper-sphere | اَبَرکره (نه «فراکره») |
| high-dimensional | با ابعاد بالا (نه «بُعد بالا») |
| curse of dimensionality | نفرین ابعاد (نه «نفرین بُعد») |
| low-rank | رتبه پایین (نه «کم‌مرتبه») |
| derivation | استنتاج (نه «اشتقاق») |

اصطلاح تازه را همین جدول اضافه کنید تا نسخه‌های بعدی یکدست بمانند.

## ۶. ساخت و بررسی

```bash
# هر دو نسخه:
python tools/build_sites.py
# فقط فارسی:
python tools/build_sites.py fa
```

روی ویندوز/git-bash (چون MSYS مقدار `/fa` را به مسیر ویندوزی تبدیل می‌کند):

```bash
MSYS_NO_PATHCONV=1 JB='C:/programs/anaconda3/envs/pth/Scripts/jupyter-book.exe' \
  python tools/build_sites.py
```

بعد از build حداقل این چهار چیز را چک کنید:

**دربارهٔ فارسی و `en`:** build انگلیسی مالک `_build/html` است و آن را پاک
می‌کند، پس `/fa/` هم از بین می‌رود. اسکریپت حالا بعد از هر build، فارسیِ قبلی را
از `fa/_build/html` دوباره کنار انگلیسی می‌گذارد (`[merge]`) و اگر آن هم نبود
هشدار `[warn]` می‌دهد؛ پس `build_sites.py en` سایت را بی‌صدا بدون فارسی رها
نمی‌کند. فقط یادتان باشد که خود `jupyter-book build --html` (دستی) این حفاظت
را ندارد.

1. `echo $?` صفر باشد و در لاگ، `[switch]` تعداد صفحات فارسی را درست بشمارد.
2. `_build/html/fa/<path>/index.html` وجود داشته باشد و در آن `dir="rtl"` باشد.
3. لینک سوییچ در صفحهٔ فارسی به نسخهٔ انگلیسی همان صفحه برود (نه به صفحهٔ اصلی):
   `grep -o '<div class="langswitch">.\{0,80\}' _build/html/fa/<path>/index.html`
4. تصویرها با پیشوند `/fa/` بار شوند: `grep -o 'src="[^"]*_public[^"]*"' ... | head`

اگر سرور پیش‌نمایش روی `_build/html` بالا است، قبل از build آن را ببندید وگرنه
ویندوز `EPERM` می‌دهد.

## ۷. تله‌های شناخته‌شده

- **فرمول‌ها با KaTeX رندر می‌شوند**، نه MathJax: `css/fa.css` باید `.katex` و
  `.katex-display` را به LTR برگرداند. اگر فقط `mjx-container` را هدف بگیرید،
  فرمول در متن راست‌به‌چپ آینه می‌شود (اعداد و اندیس‌ها جابه‌جا دیده می‌شوند).
- **داخل بلوک HTML خام، مارک‌داون کار نمی‌کند.** در چیپ سوییچ
  `**فارسی**` عیناً با همان ستاره‌ها چاپ می‌شود؛ باید `<strong>فارسی</strong>`
  بنویسید. همین برای هر HTML خام دیگری در صفحه‌ها هم صادق است.
- **`nbformat.write` کل فایل را بازقالب‌بندی می‌کند** (فهرست خط‌های `source`
  را به یک رشته تبدیل می‌کند) و diff صفحهٔ انگلیسی را شلوغ می‌کند. وقتی فقط
  چیپ را به نوتبوک انگلیسی اضافه می‌کنید، فایل را با `nbformat` ننویسید: متن
  خام JSON را بگیرید و چهار سطر رشته را قبل از `"# عنوان\\n",` در همان
  فهرست `source` وارد کنید (و بدون newline انتهایی ذخیره کنید)، بعد با
  `json.loads` اعتبارش را چک کنید. برای فایل فارسی که نو است این محدودیت
  وجود ندارد.
- `{include}` بلوک مشترک را **کار نمی‌کند** (متن خام چاپ می‌شود).
- تگ `<script>` و attributeهای `data-*` در HTML خام **حذف می‌شوند**؛ برای همین
  سوییچ با جای‌نگهدار `#lang-…` و بازنویسی در زمان build ساخته شده است.
- **build انگلیسی `_build/html/fa` را پاک می‌کند.** برای همین `tools/build_sites.py`
  پس از هر build، خروجی فارسی را دوباره کپی می‌کند و در نبودش با `[warn]`
  هشدار می‌دهد؛ اما اگر بیرون از اسکریپت build کنید، فراموش نکنید که فارسی
  را جداگانه بسازید و کپی کنید.
- MyST خودش `href`های داخلی را بازنویسی می‌کند؛ پس هیچ لینکی را با مسیر مطلق
  دستی ننویسید.
- در صفحهٔ اصلی، عنوان از `myst.yml` می‌آید و H1 صفحه بالای آن نشان داده می‌شود
  (همان رفتار نسخهٔ انگلیسی)؛ اگر H1 را حذف کنید، قالب عنوان را از اولین تیتر
  بعدی برمی‌دارد و ظاهر به‌هم می‌ریزد.
- برچسب‌های خود قالب (Contents, Search, Exercise) انگلیسی می‌مانند؛ MyST هنوز
  ترجمهٔ رابط ندارد.
- خروجی HTML تنها خروجی است؛ PDF/TeX در `myst.yml` حذف شده‌اند و ساختشان
  (و اسلایدهای reveal.js در workflow) غیرفعال است.

## ۸. نمونهٔ مرجع

`fa/high-dimensional-spaces/Clustering-Part2.ipynb` نمونهٔ کامل یک صفحهٔ دوزبانه
است: ترجمهٔ همهٔ سلول‌های markdown، کد و خروجی‌های دست‌نخورده، تصویر کپی‌شده در
`fa/high-dimensional-spaces/img/`، سوییچ دوطرفه، و مدخل فهرست در `fa/myst.yml`.
برای صفحهٔ بعدی همین را الگو بگیرید.

## ۹. وضعیت ترجمه

این فهرست با `fa/myst.yml` جلو می‌رود؛ هر صفحه‌ای که مدخل فعال دارد، ترجمه شده است:

- `fa/index.md`
- `fa/other/Course-Opening.md`
- `fa/python/Python-DSHB-intro.md`
- `fa/high-dimensional-spaces/Images-as-High-Dimensional-Data.ipynb`
- `fa/high-dimensional-spaces/Clustering-Part2.ipynb`
- `fa/high-dimensional-spaces/High-Dimensional-Spaces.md`
- `fa/high-dimensional-spaces/High-Dimensional-Data-and-The-Curse-of-Dimensionality.ipynb`
- `fa/high-dimensional-spaces/High-Dimensional-Data-and-kNN.ipynb`
- `fa/high-dimensional-spaces/High-Dimensional-Data-and-K-Means.ipynb`
- `fa/high-dimensional-spaces/Image-Clustering.ipynb`
- `fa/high-dimensional-spaces/Image-Clustering-Hierarchical.ipynb`
- `fa/linear-algebra/linear-algebra-basics.md`
- `fa/linear-algebra/Subspaces-and-Linear-Maps.md`
- `fa/linear-algebra/Projection.ipynb`
- `fa/random-graphs/Graph-Theory-Intro.md`
- `fa/other/Course-Synthesis.md`

قاعده: **صفحه‌ای که در نسخهٔ انگلیسی منتشر نشده، فارسی هم نمی‌شود** (مثلاً `IRIS-Clustering` و
`Silhouette-clustering` که در `myst.yml` انگلیسی کامنت‌اند) تا سوییچ به صفحهٔ ناموجود اشاره نکند.

پس از افزودن هر صفحهٔ تازه این را اجرا کنید تا فهرست فارسی از فهرست انگلیسی بازتولید شود؛ مدخل
هر صفحه‌ای که وجود دارد فعال و بقیه کامنت می‌شود:

```bash
python tools/sync_fa_toc.py
```
