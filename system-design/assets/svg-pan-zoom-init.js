/**
 * Initialize svg-pan-zoom on containers marked with data-svg-pan-zoom.
 * Each container should have a data-svg-src attribute pointing to the SVG file.
 * The SVG is fetched, inlined into the DOM, and then svg-pan-zoom is attached.
 */
document.addEventListener("DOMContentLoaded", function () {
  var containers = document.querySelectorAll("[data-svg-pan-zoom]");
  containers.forEach(function (container) {
    var svgSrc = container.getAttribute("data-svg-src");
    if (!svgSrc) return;

    fetch(svgSrc)
      .then(function (response) { return response.text(); })
      .then(function (svgText) {
        // Parse the SVG and insert it into the container
        var parser = new DOMParser();
        var svgDoc = parser.parseFromString(svgText, "image/svg+xml");
        var svgEl = svgDoc.documentElement;

        // Make the SVG fill the container
        svgEl.setAttribute("width", "100%");
        svgEl.setAttribute("height", "100%");
        svgEl.style.width = "100%";
        svgEl.style.height = "100%";

        container.appendChild(svgEl);

        // Initialize svg-pan-zoom
        var panZoomInstance = svgPanZoom(svgEl, {
          zoomEnabled: true,
          controlIconsEnabled: true,
          fit: true,
          center: true,
          minZoom: 0.25,
          maxZoom: 20,
          zoomScaleSensitivity: 0.3
        });

        // Handle resize
        window.addEventListener("resize", function () {
          panZoomInstance.resize();
          panZoomInstance.fit();
          panZoomInstance.center();
        });
      })
      .catch(function (err) {
        console.error("Failed to load SVG for pan-zoom:", err);
        // Fallback: show as a regular image
        var img = document.createElement("img");
        img.src = svgSrc;
        img.alt = container.getAttribute("data-svg-alt") || "SVG diagram";
        img.style.width = "100%";
        container.appendChild(img);
      });
  });
});
