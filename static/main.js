const upload = document.getElementById('imageUpload');
const maskCanvas = document.getElementById('maskCanvas');
const maskCtx = maskCanvas.getContext('2d');
const resultCanvas = document.getElementById('resultCanvas');
const resultCtx = resultCanvas.getContext('2d');
const showResult = document.getElementById('showResult');
const resetBtn = document.getElementById('resetBtn');
const sendBtn = document.getElementById('sendBtn');
const downloadBtn = document.getElementById('downloadBtn');
const downloadSection = document.getElementById('downloadSection');
const responseText = document.getElementById('responseText');
const toolSelect = document.getElementById('tool');
const brushSizeInput = document.getElementById('brushSize');
const sizeValue = document.getElementById('sizeValue');

let image = new Image();
let drawing = false;
let tool = "brush";
let brushSize = parseInt(brushSizeInput.value);

// Build a binary mask (white background, black where user painted)
function getBinaryMaskDataURL() {
  // Temp canvas with original image only (same size as maskCanvas)
  const origCanvas = document.createElement('canvas');
  origCanvas.width = maskCanvas.width;
  origCanvas.height = maskCanvas.height;
  const origCtx = origCanvas.getContext('2d');
  origCtx.drawImage(image, 0, 0, origCanvas.width, origCanvas.height);

  const origData = origCtx.getImageData(0, 0, origCanvas.width, origCanvas.height).data;
  const maskData = maskCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height).data;

  // Output mask canvas
  const out = document.createElement('canvas');
  out.width = maskCanvas.width;
  out.height = maskCanvas.height;
  const outCtx = out.getContext('2d');
  const outImg = outCtx.createImageData(out.width, out.height);

  const TH = 40; // difference threshold
  for (let i = 0; i < maskData.length; i += 4) {
    const r1 = maskData[i], g1 = maskData[i+1], b1 = maskData[i+2];
    const r0 = origData[i], g0 = origData[i+1], b0 = origData[i+2];
    // changed if any channel differs enough OR strong red painted
    const diff = Math.abs(r1 - r0) + Math.abs(g1 - g0) + Math.abs(b1 - b0);
    const painted = r1 > 180 && g1 < 80 && b1 < 80; // heuristic for red brush
    const isMask = diff > TH || painted;

    // black for mask area, white otherwise
    outImg.data[i] = isMask ? 0 : 255;
    outImg.data[i+1] = isMask ? 0 : 255;
    outImg.data[i+2] = isMask ? 0 : 255;
    outImg.data[i+3] = 255;
  }
  outCtx.putImageData(outImg, 0, 0);
  return out.toDataURL('image/png');
}

// 🖼 Handle image upload
upload.addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(evt) {
    image.onload = () => {
      // Resize the image to fit nicely
      const desiredWidth = 400;
      const scale = desiredWidth / image.width;
      const desiredHeight = image.height * scale;

      maskCanvas.width = desiredWidth;
      maskCanvas.height = desiredHeight;
      resultCanvas.width = desiredWidth;
      resultCanvas.height = desiredHeight;

      maskCtx.drawImage(image, 0, 0, desiredWidth, desiredHeight);
      resultCtx.drawImage(image, 0, 0, desiredWidth, desiredHeight);
      downloadSection.style.display = 'none'; // Hide download button on new upload
    };
    image.src = evt.target.result;
  };
  reader.readAsDataURL(file);
});

// ✏️ Drawing logic
maskCanvas.addEventListener('mousedown', () => drawing = true);
maskCanvas.addEventListener('mouseup', () => drawing = false);
maskCanvas.addEventListener('mouseleave', () => drawing = false);
maskCanvas.addEventListener('mousemove', drawMask);

// Touch support for mobile
maskCanvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  drawing = true;
});
maskCanvas.addEventListener('touchend', (e) => {
  e.preventDefault();
  drawing = false;
});
maskCanvas.addEventListener('touchmove', (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  const mouseEvent = new MouseEvent('mousemove', {
    clientX: touch.clientX,
    clientY: touch.clientY
  });
  drawMask(mouseEvent);
});

function drawMask(e) {
  if (!drawing) return;

  const rect = maskCanvas.getBoundingClientRect();
  const scaleX = maskCanvas.width / rect.width;
  const scaleY = maskCanvas.height / rect.height;

  const x = (e.clientX - rect.left) * scaleX;
  const y = (e.clientY - rect.top) * scaleY;

  if (tool === "brush") {
    maskCtx.fillStyle = "rgba(255,0,0,0.4)";
    maskCtx.beginPath();
    maskCtx.arc(x, y, brushSize, 0, Math.PI * 2);
    maskCtx.fill();
  } else if (tool === "eraser") {
    maskCtx.globalCompositeOperation = "destination-out";
    maskCtx.beginPath();
    maskCtx.arc(x, y, brushSize, 0, Math.PI * 2);
    maskCtx.fill();
    maskCtx.globalCompositeOperation = "source-over";
  }
}

// 🔧 Tool and size controls
toolSelect.addEventListener('change', e => tool = e.target.value);
brushSizeInput.addEventListener('input', e => {
  brushSize = parseInt(e.target.value);
  sizeValue.textContent = brushSize;
});

// 🧹 Clear mask
resetBtn.addEventListener('click', () => {
  if (!image.src) return;
  maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);
  maskCtx.drawImage(image, 0, 0, maskCanvas.width, maskCanvas.height);
  resultCtx.drawImage(image, 0, 0, resultCanvas.width, resultCanvas.height);
});

// 🖼 Show result overlay
showResult.addEventListener('click', () => {
  resultCtx.drawImage(image, 0, 0, resultCanvas.width, resultCanvas.height);
  resultCtx.drawImage(maskCanvas, 0, 0, maskCanvas.width, maskCanvas.height);
});

// 🚀 Send to backend
sendBtn.addEventListener('click', async () => {
  if (!image.src) {
    alert("Upload an image first!");
    return;
  }

  const originalData = image.src;
  // Build a clean binary mask instead of sending the overlaid canvas
  const maskData = getBinaryMaskDataURL();

  responseText.textContent = "Generating...";
  downloadSection.style.display = 'none'; // Hide download button while processing

  const res = await fetch("/upload_mask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ original: originalData, mask: maskData })
  });

  if (!res.ok) {
    responseText.textContent = `❌ Error ${res.status}`;
    return;
  }

  const ct = res.headers.get('Content-Type') || '';
  // If backend returns PNG, draw it onto canvas; otherwise show text
  if (ct.includes('image/png')) {
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const img = new Image();
    img.onload = () => {
      // Fit into a visible 300x300 canvas
      const CAN = 300;
      resultCanvas.width = CAN;
      resultCanvas.height = CAN;
      resultCtx.fillStyle = '#fff';
      resultCtx.fillRect(0, 0, CAN, CAN);
      const scale = Math.min(CAN / img.width, CAN / img.height);
      const w = Math.round(img.width * scale);
      const h = Math.round(img.height * scale);
      const x = Math.floor((CAN - w) / 2);
      const y = Math.floor((CAN - h) / 2);
      resultCtx.drawImage(img, x, y, w, h);
      responseText.textContent = '✅ Image generated successfully!';
      downloadSection.style.display = 'block'; // Show download button
      URL.revokeObjectURL(url);
    };
    img.onerror = () => {
      responseText.textContent = '❌ Failed to load result image';
    };
    img.src = url;
  } else {
    // Fallback: show text (maybe error JSON)
    try {
      const data = await res.json();
      responseText.textContent = data.error || JSON.stringify(data);
    } catch (e) {
      responseText.textContent = await res.text();
    }
  }
});

// 💾 Download functionality
downloadBtn.addEventListener('click', () => {
  // Create a temporary link element to trigger download
  const link = document.createElement('a');
  link.download = 'inpainted-image.png';
  link.href = resultCanvas.toDataURL('image/png');
  
  // Trigger the download
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
});
