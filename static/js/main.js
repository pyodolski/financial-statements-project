// 파일 업로드 처리
const uploadBox = document.getElementById("uploadBox");
const fileInput = document.getElementById("fileInput");
const progress = document.getElementById("progress");
const result = document.getElementById("result");

// 드래그 앤 드롭
uploadBox.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadBox.classList.add("dragover");
});

uploadBox.addEventListener("dragleave", () => {
  uploadBox.classList.remove("dragover");
});

uploadBox.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadBox.classList.remove("dragover");

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFile(files[0]);
  }
});

// 파일 선택
fileInput.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    handleFile(e.target.files[0]);
  }
});

// 파일 처리
function handleFile(file) {
  if (!file.name.endsWith(".xlsx")) {
    alert("Excel 파일(.xlsx)만 업로드 가능합니다.");
    return;
  }

  uploadFile(file);
}

// 파일 업로드
async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  // UI 업데이트
  uploadBox.style.display = "none";
  progress.style.display = "block";

  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      showResult(data);
    } else {
      throw new Error(data.error || "변환 중 오류가 발생했습니다.");
    }
  } catch (error) {
    alert("오류: " + error.message);
    location.reload();
  }
}

// 결과 표시
function showResult(data) {
  progress.style.display = "none";
  result.style.display = "block";

  // 갱신 메시지 표시
  if (data.updated && data.result.transaction_period) {
    const updateNotice = document.createElement("div");
    updateNotice.style.cssText =
      "background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 12px; border-radius: 4px; margin-bottom: 15px;";
    updateNotice.innerHTML = `✓ <strong>거래기간 "${data.result.transaction_period}"</strong>의 기존 데이터가 새로운 파일로 갱신되었습니다.`;
    result.insertBefore(updateNotice, result.firstChild);
  }

  // 숫자 포맷팅
  const formatNumber = (num) => {
    return new Intl.NumberFormat("ko-KR").format(Math.round(num)) + "원";
  };

  document.getElementById("totalSales").textContent = formatNumber(
    data.result.total_maechul
  );
  document.getElementById("totalCost").textContent = formatNumber(
    data.result.maechul_wonka
  );
  document.getElementById("grossProfit").textContent = formatNumber(
    data.result.maechul_total_iik
  );
  document.getElementById("depositAmount").textContent = formatNumber(
    data.result.ipgeum_total
  );

  // 다운로드 버튼
  const downloadBtn = document.getElementById("downloadBtn");
  downloadBtn.onclick = () => {
    window.location.href = "/download/" + data.output_filename;
  };
}
