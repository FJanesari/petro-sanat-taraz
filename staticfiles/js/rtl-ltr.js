document.addEventListener("DOMContentLoaded", function () {
  const lang = localStorage.getItem("preferredLang") || "fa";
  const htmlTag = document.documentElement;

  // تعیین زبان و جهت نوشتار
  htmlTag.setAttribute("lang", lang);
  htmlTag.setAttribute("dir", lang === "fa" || lang === "ar" ? "rtl" : "ltr");

  // حذف کلاس قبلی از body
  document.body.classList.remove("rtl", "ltr");
  document.body.classList.add(lang === "fa" || lang === "ar" ? "rtl" : "ltr");

  // حذف لینک‌های موجود
  const existingRtlLink = document.getElementById("rtl-style");
  if (existingRtlLink) existingRtlLink.remove();

  const existingLtrLink = document.getElementById("ltr-style");
  if (existingLtrLink) existingLtrLink.remove();

  // لود فایل مناسب
  if (lang === "fa" || lang === "ar") {
    const rtlLink = document.createElement("link");
    rtlLink.id = "rtl-style";
    rtlLink.rel = "stylesheet";
    rtlLink.href = "assets/css/rtl.css";
    document.head.appendChild(rtlLink);
  } else {
    const ltrLink = document.createElement("link");
    ltrLink.id = "ltr-style";
    ltrLink.rel = "stylesheet";
    ltrLink.href = "assets/css/ltr.css";
    document.head.appendChild(ltrLink);
  }
});
