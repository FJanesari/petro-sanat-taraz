// let BASE_API_URL;

// const IS_LOCAL =
//   window.location.hostname === "127.0.0.1" ||
//   window.location.hostname === "localhost";

// if (IS_LOCAL) {
//   BASE_API_URL = "http://localhost:8000";
// } else if (window.location.hostname === "host.docker.internal") {
//   BASE_API_URL = "http://localhost:8000";
// } else {
//   BASE_API_URL = "https://domain.com"; // پروDUCTION
// }

// /* ---------------------------
//    فقط در لوکال: بازنویسی لینک‌های /fa/ به فایل‌های .html
//    هم روی DOM موجود اعمال می‌کنیم، هم کلیک‌ها را اینترسپت می‌کنیم
// --------------------------- */

// function faPathToLocalFile(href) {
//   try {
//     // مطمئن می‌شیم با origin حل بشه (برای لینک‌های نسبی/مطلق)
//     const u = new URL(href, window.location.origin);

//     // فقط لینک‌هایی که با /fa/ شروع می‌شن
//     if (!u.pathname.startsWith("/fa/")) return null;

//     // مسیر بعد از fa/
//     let path = u.pathname.replace(/^\/fa\//, "");     // contact/ یا blog/slug/ یا blog-details/
//     path = path.replace(/\/+$/, "");                  // حذف اسلش انتهایی

//     // هندر بلاگ: /fa/blog/<slug>/  → blog-details.html?slug=<slug>
//     const mBlog = path.match(/^blog\/([^/]+)$/);
//     if (mBlog) {
//       const slug = mBlog[1].replace(/\/+$/, "");
//       return `blog-details.html?slug=${slug}${u.hash || ""}`;
//     }

//     // هندر اباوت: /fa/about/<slug>/ → about.html?slug=<slug>
//     const mAbout = path.match(/^about\/([^/]+)$/);
//     if (mAbout) {
//       const slug = mAbout[1].replace(/\/+$/, "");
//       return `about.html?slug=${slug}${u.hash || ""}`;
//     }

//     // اگر لینک از نوع /fa/blog-details/?slug=... بود → blog-details.html?slug=...
//     if (path.startsWith("blog-details")) {
//       return `blog-details.html${u.search}${u.hash || ""}`;
//     }

//     // اگر لینک از نوع /fa/about.html?slug=... بود → همونه
//     if (path.startsWith("about.html")) {
//       return `about.html${u.search}${u.hash || ""}`;
//     }

//     // سایر صفحات ساده: /fa/contact/ → contact.html
//     return `${path}.html${u.search || ""}${u.hash || ""}`;
//   } catch (e) {
//     return null;
//   }
// }

// if (IS_LOCAL) {
//   // 1) بازنویسی اولیه‌ی href ها (آنچه تا الان داخل DOM هست)
//   document.addEventListener("DOMContentLoaded", function () {
//     document.querySelectorAll("a[href^='/fa/']").forEach((a) => {
//       const newHref = faPathToLocalFile(a.getAttribute("href"));
//       if (newHref) a.setAttribute("href", newHref);
//     });
//   });

//   // 2) پوشش لینک‌های داینامیک (که بعداً با JS ساخته می‌شن) با MutationObserver
//   document.addEventListener("DOMContentLoaded", function () {
//     const obs = new MutationObserver((muts) => {
//       muts.forEach((m) => {
//         m.addedNodes.forEach((node) => {
//           if (node.nodeType !== 1) return;
//           // خود node یا فرزندانش اگر <a> باشند
//           if (node.matches && node.matches("a[href^='/fa/']")) {
//             const newHref = faPathToLocalFile(node.getAttribute("href"));
//             if (newHref) node.setAttribute("href", newHref);
//           }
//           node.querySelectorAll &&
//             node.querySelectorAll("a[href^='/fa/']").forEach((a) => {
//               const newHref = faPathToLocalFile(a.getAttribute("href"));
//               if (newHref) a.setAttribute("href", newHref);
//             });
//         });
//       });
//     });
//     obs.observe(document.documentElement, { childList: true, subtree: true });
//   });

//   // 3) اینترسپت کلیک (حتی اگر اسکریپت دیگری بعداً href را عوض کند)
//   document.addEventListener(
//     "click",
//     function (e) {
//       const a = e.target.closest && e.target.closest("a");
//       if (!a) return;

//       const hrefAttr = a.getAttribute("href");
//       if (!hrefAttr) return;

//       // فقط لینک‌های /fa/
//       if (!hrefAttr.startsWith("/fa/")) return;

//       const newHref = faPathToLocalFile(hrefAttr);
//       if (!newHref) return;

//       e.preventDefault();
//       window.location.href = newHref;
//     },
//     true // capture تا قبل از هندلرهای دیگر عمل کند
//   );
// }




let BASE_API_URL;

if (window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost") {
  BASE_API_URL = "http://localhost:8000";
} else {
  BASE_API_URL = "https://test-seo.petrosanattaraz.com";
}


function getSlugAndLang() {
  const pathParts = window.location.pathname.split("/").filter(Boolean);

  // مسیرهایی که زبان نباید روشون اعمال بشه
  const excludedPaths = ["admin", "api"];

  let lang = "fa"; // پیش‌فرض
  let slug = null;

  if (pathParts.length > 0 && !excludedPaths.includes(pathParts[0])) {
    lang = pathParts[0];
    // برای صفحات جزئیات (مثلاً blog-details یا product-details)
    slug = pathParts.length > 2 ? pathParts[2] : null;
  }

  return { lang, slug };
}
