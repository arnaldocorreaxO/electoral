(async () => {
  const res = await fetch("/static/version.json", { cache: "no-store" });
  const version = await res.json();

  // Versionar TODOS los CSS
  document.querySelectorAll('link[rel="stylesheet"]').forEach((link) => {
    if (link.href.includes(".css")) {
      const url = new URL(link.href);
      url.searchParams.set("v", version.css);
      link.href = url.toString();
    }
  });

  // Versionar TODOS los JS EXCEPTO este script
  document.querySelectorAll("script[src]").forEach((script) => {
    if (
      script.src.includes(".js") &&
      !script.src.includes("version.js") && // ← EVITA EL LOOP
      !script.src.includes("versioning.js") // ← por si usás otro nombre
    ) {
      const url = new URL(script.src);
      url.searchParams.set("v", version.js);

      const newScript = document.createElement("script");
      newScript.src = url.toString();
      script.replaceWith(newScript);
    }
  });
})();
