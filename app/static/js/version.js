(async () => {
  // 1) Leer version.json sin caché
  const res = await fetch("/static/version.json", { cache: "no-store" });
  const version = await res.json();

  // 2) Versionar SOLO CSS dentro de /static/css/
  document.querySelectorAll('link[rel="stylesheet"]').forEach((link) => {
    if (link.href.includes("/static/css/")) {
      const url = new URL(link.href);
      url.searchParams.set("v", version.css);
      link.href = url.toString();
    }
  });

  // 3) Versionar SOLO JS dentro de /static/js/
  document.querySelectorAll("script[src]").forEach((script) => {
    if (
      script.src.includes("/static/js/") &&
      !script.src.includes("version") // evita versionar este mismo script
    ) {
      const url = new URL(script.src);
      url.searchParams.set("v", version.js);

      const newScript = document.createElement("script");
      newScript.src = url.toString();
      script.replaceWith(newScript);
    }
  });
})();
