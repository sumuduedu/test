const cookieName = "mitc_attendee_profile";
const logKey = "mitc_attendance_log";

const modal = document.getElementById("attendee-modal");
const openAttendee = document.getElementById("open-attendee");
const closeAttendee = document.getElementById("close-attendee");
const saveAttendee = document.getElementById("save-attendee");
const profileStatus = document.getElementById("profile-status");

const sessionName = document.getElementById("session-name");
const trainerName = document.getElementById("trainer-name");
const sessionRoom = document.getElementById("session-room");
const generateQr = document.getElementById("generate-qr");
const qrCanvas = document.getElementById("qr-canvas");
const qrMeta = document.getElementById("qr-meta");
const sessionCodeField = document.getElementById("session-code");
const copySession = document.getElementById("copy-session");
const qrStatus = document.getElementById("qr-status");

const startScan = document.getElementById("start-scan");
const stopScan = document.getElementById("stop-scan");
const scanStatus = document.getElementById("scan-status");
const manualCode = document.getElementById("manual-code");
const submitManual = document.getElementById("submit-manual");

const attendanceBody = document.getElementById("attendance-body");
const clearLog = document.getElementById("clear-log");
const exportLog = document.getElementById("export-log");

let html5QrCode = null;

const defaultProfile = {
  name: "",
  course: "",
  id: "",
};

const readCookie = (name) => {
  const match = document.cookie
    .split(";")
    .map((value) => value.trim())
    .find((value) => value.startsWith(`${name}=`));
  if (!match) {
    return null;
  }
  return decodeURIComponent(match.split("=")[1]);
};

const writeCookie = (name, value, days = 30) => {
  const expires = new Date(Date.now() + days * 86400000).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
};

const getProfile = () => {
  const stored = readCookie(cookieName);
  if (!stored) {
    return { ...defaultProfile };
  }
  try {
    return { ...defaultProfile, ...JSON.parse(stored) };
  } catch (error) {
    return { ...defaultProfile };
  }
};

const setProfile = (profile) => {
  writeCookie(cookieName, JSON.stringify(profile));
};

const openModal = () => {
  modal.classList.add("show");
  modal.setAttribute("aria-hidden", "false");
};

const closeModal = () => {
  modal.classList.remove("show");
  modal.setAttribute("aria-hidden", "true");
};

const populateProfile = () => {
  const profile = getProfile();
  document.getElementById("trainee-name").value = profile.name;
  document.getElementById("trainee-course").value = profile.course;
  document.getElementById("trainee-id").value = profile.id;
};

const getAttendanceLog = () => {
  const stored = localStorage.getItem(logKey);
  if (!stored) {
    return [];
  }
  try {
    return JSON.parse(stored);
  } catch (error) {
    return [];
  }
};

const setAttendanceLog = (items) => {
  localStorage.setItem(logKey, JSON.stringify(items));
};

const renderLog = () => {
  const log = getAttendanceLog();
  attendanceBody.innerHTML = "";
  if (log.length === 0) {
    attendanceBody.innerHTML = "<tr><td colspan='7'>No attendance captured yet.</td></tr>";
    return;
  }
  log.forEach((entry) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${entry.timestamp}</td>
      <td>${entry.sessionName}</td>
      <td>${entry.trainerName}</td>
      <td>${entry.room}</td>
      <td>${entry.traineeName}</td>
      <td>${entry.course}</td>
      <td>${entry.id}</td>
    `;
    attendanceBody.appendChild(row);
  });
};

const buildSessionPayload = () => {
  const payload = {
    sessionName: sessionName.value.trim() || "NVQ Session",
    trainerName: trainerName.value.trim() || "Trainer",
    room: sessionRoom.value.trim() || "Room",
    timestamp: new Date().toISOString(),
  };
  return payload;
};

const setQrMeta = (payload) => {
  const date = new Date(payload.timestamp);
  qrMeta.textContent = `Session: ${payload.sessionName} | Trainer: ${payload.trainerName} | ${payload.room} | ${date.toLocaleString()}`;
};

const setSessionCode = (payload) => {
  sessionCodeField.value = JSON.stringify(payload);
};

const parsePayload = (value) => {
  const trimmed = value.trim();
  if (!trimmed) {
    return null;
  }
  try {
    return JSON.parse(trimmed);
  } catch (error) {
    try {
      const decoded = decodeURIComponent(atob(trimmed));
      return JSON.parse(decoded);
    } catch (decodeError) {
      return null;
    }
  }
};

const generateQrCode = async () => {
  const payload = buildSessionPayload();
  const text = JSON.stringify(payload);
  setSessionCode(payload);
  setQrMeta(payload);
  if (typeof QRCode === "undefined") {
    qrStatus.textContent = "QR library failed to load. Share the session code manually.";
    return;
  }
  await QRCode.toCanvas(qrCanvas, text, {
    width: 180,
    margin: 1,
    color: {
      dark: "#0f172a",
      light: "#f8fafc",
    },
  });
  qrStatus.textContent = "QR ready. Ask trainees to scan or use the session code.";
};

const addAttendanceEntry = (sessionPayload) => {
  const profile = getProfile();
  if (!profile.name || !profile.course || !profile.id) {
    profileStatus.textContent = "Please complete your trainee profile first.";
    openModal();
    return false;
  }
  const entry = {
    timestamp: new Date().toLocaleString(),
    sessionName: sessionPayload.sessionName,
    trainerName: sessionPayload.trainerName,
    room: sessionPayload.room,
    traineeName: profile.name,
    course: profile.course,
    id: profile.id,
  };
  const log = getAttendanceLog();
  log.unshift(entry);
  setAttendanceLog(log);
  renderLog();
  scanStatus.textContent = `Attendance captured for ${profile.name}.`;
  return true;
};

const handleScanSuccess = (decodedText) => {
  const payload = parsePayload(decodedText);
  if (payload) {
    addAttendanceEntry(payload);
    return;
  }
  scanStatus.textContent = "Invalid QR payload. Ask the trainer to regenerate the QR.";
};

const startScanner = async () => {
  if (!html5QrCode) {
    html5QrCode = new Html5Qrcode("scanner");
  }
  scanStatus.textContent = "Starting scanner...";
  try {
    await html5QrCode.start(
      { facingMode: "environment" },
      { fps: 10, qrbox: 200 },
      (decodedText) => {
        handleScanSuccess(decodedText);
      }
    );
    scanStatus.textContent = "Scanner active. Point at the QR code.";
  } catch (error) {
    scanStatus.textContent = "Unable to access camera. Use manual entry instead.";
  }
};

const stopScanner = async () => {
  if (!html5QrCode) {
    return;
  }
  try {
    await html5QrCode.stop();
    scanStatus.textContent = "Scanner stopped.";
  } catch (error) {
    scanStatus.textContent = "Scanner already stopped.";
  }
};

const handleManualSubmit = () => {
  const value = manualCode.value.trim();
  if (!value) {
    scanStatus.textContent = "Enter a session code to submit attendance.";
    return;
  }
  const payload = parsePayload(value);
  if (payload) {
    addAttendanceEntry(payload);
    return;
  }
  scanStatus.textContent = "Manual code is invalid. Paste the full session code.";
};

const handleExport = () => {
  const log = getAttendanceLog();
  if (log.length === 0) {
    scanStatus.textContent = "No attendance entries to export.";
    return;
  }
  const headers = [
    "Timestamp",
    "Session",
    "Trainer",
    "Room",
    "Trainee",
    "Course",
    "NIC/Student ID",
  ];
  const rows = log.map((entry) => [
    entry.timestamp,
    entry.sessionName,
    entry.trainerName,
    entry.room,
    entry.traineeName,
    entry.course,
    entry.id,
  ]);
  const csv = [headers, ...rows]
    .map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(","))
    .join("\n");
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "mitc-attendance.csv";
  link.click();
  URL.revokeObjectURL(url);
};

const handleClearLog = () => {
  setAttendanceLog([]);
  renderLog();
};

openAttendee.addEventListener("click", () => {
  populateProfile();
  openModal();
});

closeAttendee.addEventListener("click", () => {
  closeModal();
});

saveAttendee.addEventListener("click", () => {
  const profile = {
    name: document.getElementById("trainee-name").value.trim(),
    course: document.getElementById("trainee-course").value.trim(),
    id: document.getElementById("trainee-id").value.trim(),
  };
  if (!profile.name || !profile.course || !profile.id) {
    profileStatus.textContent = "Please complete all fields before saving.";
    return;
  }
  setProfile(profile);
  profileStatus.textContent = "Profile saved. You can now scan the QR.";
  closeModal();
});

modal.addEventListener("click", (event) => {
  if (event.target === modal) {
    closeModal();
  }
});

generateQr.addEventListener("click", () => {
  generateQrCode();
});

startScan.addEventListener("click", () => {
  startScanner();
});

stopScan.addEventListener("click", () => {
  stopScanner();
});

submitManual.addEventListener("click", () => {
  handleManualSubmit();
});

exportLog.addEventListener("click", () => {
  handleExport();
});

clearLog.addEventListener("click", () => {
  handleClearLog();
});

copySession.addEventListener("click", async () => {
  if (!sessionCodeField.value) {
    qrStatus.textContent = "Generate a session code first.";
    return;
  }
  try {
    await navigator.clipboard.writeText(sessionCodeField.value);
    qrStatus.textContent = "Session code copied.";
  } catch (error) {
    sessionCodeField.select();
    qrStatus.textContent = "Copy failed. Select the code and copy manually.";
  }
});

window.addEventListener("load", () => {
  populateProfile();
  renderLog();
  generateQrCode();
  const profile = getProfile();
  if (!profile.name) {
    openModal();
  }
});
