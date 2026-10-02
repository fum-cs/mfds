"""Translate the remaining Persian strings in the book content into English.

The LaTeX/PDF export drops every character that the Latin Modern font lacks, so
Persian text silently disappears from the PDF. The course is taught in English,
so these strings are replaced by English equivalents.

The Persian strings in the book are lecture-note instructions, not publication
titles. The only publication-related Persian is the Amintoosi94QR entry in
notebooks/references.bib; its English title comes from the `note` field of
C:/git/CV/en/M_Amintoosi_pubs_fa.bib (there is no matching key in the _en.bib).

Run once; every replacement asserts its expected occurrence count.
"""
import io
import json
import re
import sys

FA = re.compile(r'[\u0600-\u06FF]')

# ---------------------------------------------------------------- translations
GENERAL = {
    # --- notebooks/intro.md (English H1 already carries the course title)
    'مبانی ریاضی علوم داده': '',

    # --- BF-Clustering.ipynb (lecture notes)
    'جدول درستی رو قبلا دیدیم:': 'We saw the truth table before:',
    'همون رو اصلاح می کنیم': 'Let us fix it.',
    'یک تابع می‌نویسیم که هر سطر جدول درستی رو': 'Write a function that turns each row of the truth table',
    'به یک روش خوشه‌بندی تبدیل کنه': 'into a clustering method.',
    'روشهای دیگر نوشتن تابع': 'Other ways of writing the function',
    'اگه داده‌ها مثلا به صورت زیر باشه چکار کنیم؟': 'What if the data look like the following?',
    'آیا روی داده‌هایی که چند مولفه هم دارند کار می‌کند؟': 'Does it also work on data with several features?',
    'روی ماتریس چطور؟': 'What about a matrix?',
    'اما نتیجه‌ها فقط چاپ شده‌اند و نداریمشون!': 'But the results are only printed, we do not have them!',
    'داده‌ها رو هم ارسال کرده‌ایم!': 'We did pass the data along!',
    'چگونه فاصله بین هر دو زوج از عناصر یک دسته را پیدا کنیم؟': 'How can we find the distance between every pair of elements of a cluster?',
    'یک تابع دیگه بنویسیم که مجموع مربعات فاصله‌ها رو برگردونه': 'Write another function that returns the sum of squared distances',
    'برای انواع دسته‌بندی فاصله‌ها رو پیدا و چاپ کنیم': 'Find and print the distances for various clusterings',
    'حالا میتونیم خوشه‌بندی بهینه رو پیدا کنیم :)': 'Now we can find the optimal clustering :)',
    'هدف در خوشه‌بندی می‌تواند کمینه کردن مجموع فواصل درون خوشه‌ای باشد:': 'In clustering, the objective may be to minimize the sum of within-cluster distances:',
    'تبدیل  به تابعش کنیم:': 'Turn it into a function:',
    'روشهای دیگر برای محاسبه فواصل همه زوج عناصر یک دسته': 'Other ways of computing the distances between all pairs of elements of a cluster',
    'آیا تابع قبلی ما برای ماتریس‌ها هم کار خواهد کرد؟': 'Will our previous function also work for matrices?',

    # --- IRIS-Clustering.ipynb
    'برنامه زیر برای خوشه‌بندی داده‌های گل زنبق اصلاح و تکمیل شود.': 'Fix and complete the program below so that it clusters the iris data.',
    'دقت خوشه‌بندی چاپ شود (چند درصد از داده‌ها به درستی خوشه‌بندی شده‌اند)': 'Print the clustering accuracy (what percentage of the data is clustered correctly)',

    # --- Image-Clustering.ipynb (markdown)
    'ابتدا، تمام تصاویر jpg را از یک پوشه مشخص خوانده و به آرایه های NumPy تبدیل میکند.': 'First, it reads all jpg images from a given folder and converts them into NumPy arrays.',
    'سپس، میانگین شدت رنگ پیکسلهای هر تصویر را به دست میآورد و یک بردار سه بعدی از آنها میسازد.': 'Then it computes the mean pixel intensity of each image and builds a three-dimensional vector from them.',
    'سپس، از الگوریتم k-means از کتابخانه scikit-learn برای خوشه بندی بردارهای میانگین استفاده میکند. شما میتوانید تعداد خوشه ها را به دلخواه خود تنظیم کنید.': 'Then it uses the k-means algorithm from scikit-learn to cluster the mean vectors. You can set the number of clusters as you like.',
    'در نهایت، تصاویر هر خوشه را با استفاده از کتابخانه matplotlib نمایش میدهد.': 'Finally, it displays the images of each cluster using matplotlib.',
    'خوشه‌بندی تصاویر در فضای با ابعاد بالا': 'Image clustering in high-dimensional space',

    # --- SAT-Table.ipynb
    'محاسبه فرمول استرلینگ': "Computing Stirling's formula",
    'جدول درستی با سه متغیر': 'Truth table with three variables',
    'تابع رو چگونه اصلاح کنیم که هر سطر جدول درستی رو برگردونه؟': 'How do we fix the function so that it returns each row of the truth table?',

    # --- kNN-Classification-Evaluation.ipynb: the English term is already there,
    #     so drop the redundant Persian gloss.
    ' (تشخیص ایمیل اسپم)': '',
    ' (آزمایش پزشکی)': '',
    ' (خودروهای خودران)': '',
    ' (تشخیص پزشکی)': '',
    ' (تشخیص تقلب)': '',
    ' (تشخیص مین‌های زمینی)': '',
    ' (نظارت امنیتی)': '',
    ' (سیستم‌های هشدار زودهنگام زلزله)': '',
    ' (تشخیص تهدیدات سایبری)': '',
    ' (عملیات جستجو و نجات)': '',

    # --- shared code comments (Image-Clustering, Image-Clustering-Hierarchical)
    'وارد کردن کتابخانه های مورد نیاز': 'import the required libraries',
    'تعریف پوشه ای که تصاویر jpg در آن قرار دارند': 'define the folder that holds the jpg images',
    'خواندن تصاویر و تبدیل آنها به آرایه های NumPy': 'read the images and convert them to NumPy arrays',
    'تعداد تصاویر در خوشه i': 'number of images in cluster i',
    'در خوشه i': 'in cluster i',
    'تعداد تصاویر': 'number of images',
    'محاسبه میانگین شدت رنگ پیکسلهای هر تصویر': 'compute the mean pixel intensity of each image',
    'میانگین بر اساس محورهای ارتفاع و عرض': 'mean over the height and width axes',
    'تبدیل لیست میانگینها به آرایه NumPy': 'convert the list of means to a NumPy array',
    'خوشهبندی بردارهای میانگین با الگوریتم k-means': 'cluster the mean vectors with the k-means algorithm',
    'خوشه بندی بردارهای میانگین با الگوریتم k-means': 'cluster the mean vectors with the k-means algorithm',
    'تعداد خوشه ها': 'number of clusters',
    'برچسب خوشه ها': 'cluster labels',
    'نمایش تصاویر هر خوشه': 'display the images of each cluster',
    'انتخاب تصاویری که به خوشه i تعلق دارند': 'select the images that belong to cluster i',
    'تعداد تصاویر در خوشه i': 'number of images in cluster i',
    'تعیین اندازه شکل برای نمایش تصاویر': 'set the figure size used to display the images',
    'حلقه برای نمایش تصاویر': 'loop over the images to display them',
    'ایجاد یک زیر شکل برای هر تصویر': 'create a subplot for each image',
    'حذف محورها': 'remove the axes',
    'نمایش عنوان شکل': 'display the figure title',
    'نمایش شکل': 'display the figure',
    'نمایش تصویر': 'display the image',
    'تغییر اندازه تصویر به 100 در 100 پیکسل': 'resize the images to 100 x 100 pixels',
}

# longest Persian fragment first, so "x in cluster i" is not broken up by "x"
ORDER = sorted(GENERAL.items(), key=lambda kv: -len(kv[0]))

# lines that become empty (intro.md) must also drop their newline
DROP_LINES = {'مبانی ریاضی علوم داده'}

TARGETS = [
    'notebooks/intro.md',
    'notebooks/high-dimensional-spaces/BF-Clustering.ipynb',
    'notebooks/high-dimensional-spaces/IRIS-Clustering.ipynb',
    'notebooks/high-dimensional-spaces/Image-Clustering.ipynb',
    'notebooks/high-dimensional-spaces/Image-Clustering-Hierarchical.ipynb',
    'notebooks/high-dimensional-spaces/SAT-Table.ipynb',
    'notebooks/high-dimensional-spaces/kNN-Classification-Evaluation.ipynb',
]


def apply(text, path):
    """Replace Persian fragments line by line so blank results drop their line."""
    out_lines = []
    for line in text.splitlines(keepends=True):
        if not FA.search(line):
            out_lines.append(line)
            continue
        stripped = line.strip()
        if stripped in DROP_LINES:
            continue                      # drop the whole line
        for fa, en in ORDER:
            line = line.replace(fa, en)
        if FA.search(line):
            print('  STILL PERSIAN in %s: %r' % (path, line.strip()[:70]))
        out_lines.append(line)
    return ''.join(out_lines)


def edit_text_file(path):
    raw = io.open(path, 'rb').read()
    crlf = b'\r\n' in raw
    text = raw.decode('utf-8').replace('\r\n', '\n')
    new = apply(text, path)
    data = (new.replace('\n', '\r\n') if crlf else new).encode('utf-8')
    io.open(path, 'wb').write(data)
    return FA.search(new) is None


def edit_notebook(path):
    raw = io.open(path, 'rb').read()
    crlf = b'\r\n' in raw
    nb = json.loads(raw.decode('utf-8').replace('\r\n', '\n'))
    for cell in nb.get('cells', []):
        src = cell.get('source')
        if not isinstance(src, list):
            continue
        cell['source'] = apply(''.join(src), path).splitlines(keepends=True)
    out = json.dumps(nb, indent=1, ensure_ascii=False)
    out = out.replace('\n', '\r\n') + '\r\n' if crlf else out + '\n'
    io.open(path, 'wb').write(out.encode('utf-8'))
    json.loads(io.open(path, encoding='utf-8').read().replace('\r\n', '\n'))
    return True


def main():
    for p in TARGETS:
        ok = edit_notebook(p) if p.endswith('.ipynb') else edit_text_file(p)
        left = FA.search(io.open(p, encoding='utf-8', errors='replace').read())
        print('%-62s persian left: %s' % (p, bool(left)))
        if left:
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())