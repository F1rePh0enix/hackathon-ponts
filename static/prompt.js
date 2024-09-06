const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");
const uploadForm = document.getElementById('upload-form');
const uploadStatus = document.getElementById('upload-status');
const chargerDoc = document.getElementById('charger-doc')
const bodyTheme = document.getElementById('body');
const DMButton = document.getElementById('dark-mode');
const audio = document.getElementById('audio-player');
const resetButton = document.getElementById('reset-button')
audio.volume = 0.8;

const appendHumanMessage = (message) => {
  const humanMessageElement = document.createElement("div");
  humanMessageElement.classList.add("message", "message-human");
  humanMessageElement.innerHTML = message;
  messagesContainer.appendChild(humanMessageElement);
};

const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};


const handlePrompt = async (event) => {
  audio.play()
  uploadStatus.innerText = '';
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();

  let url = "/prompt";
  if (questionButton.dataset.question !== undefined) {
    url = "/answer";
    data.append("question", questionButton.dataset.question);
    delete questionButton.dataset.question;
    questionButton.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }

  appendHumanMessage(data.get("prompt"));

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.answer;
  });
};

promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async (event) => {
  audio.play()
  uploadStatus.innerText = '';
  appendAIMessage(async () => {
    const response = await fetch("/question", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "Répondre à la question";
    return question;
  });
};

questionButton.addEventListener("click", handleQuestionClick);


const HandleDarkModeClick = async (event) => {
  audio.play()
  uploadStatus.innerText = '';
  console.log('DM button pressed');
  let url = "/dark";
  if (bodyTheme.classList.contains("lightmode")) {
    bodyTheme.classList.remove("lightmode");
    bodyTheme.classList.add("darkmode");
  }
  else {
    bodyTheme.classList.remove("darkmode");
    bodyTheme.classList.add("lightmode");
  }
};

DMButton.addEventListener("click", HandleDarkModeClick);


const HandleResetClick = async (event) => {
  audio.play()
  uploadStatus.innerText = '';
  console.log('reset button pressed');
  try {
    const response = await fetch("/reset", {
      method: 'POST',
      body: "",
    });

    if (response.ok) {
      console.log('Reset successful');
    } else {
      console.log('Reset failed');
    }
  } catch (error) {
    console.error('Error during reset:', error);
  }
};

resetButton.addEventListener("click", HandleResetClick);

uploadForm.addEventListener('submit', async (event) => {
  uploadStatus.innerText = '';
  audio.play()
  event.preventDefault();

  const formData = new FormData(uploadForm);
  const fileInput = document.getElementById('file-upload');
  const file = fileInput.files[0];

  // Vérifier si le fichier est de type PDF, TXT ou DOCX
  const allowedTypes = ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  if (file && allowedTypes.includes(file.type)) {
    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json()
      console.log(result)

      if (response.ok) {

        uploadStatus.innerText = 'Fichier téléchargé avec succès !';
      } else {
        uploadStatus.innerText = 'Échec du téléchargement du fichier.';
      }
    } catch (error) {
      uploadStatus.innerText = 'Une erreur est survenue lors du téléchargement.';
    }
  } else {
    uploadStatus.innerText = 'Veuillez sélectionner un fichier PDF, TXT ou DOCX.';
  }
});


const handleChargerClick = async (event) => {
  audio.play()
  uploadStatus.innerText = '';
  // Élément sélectionné
  var selectElement = document.getElementById('menu-depliant');

  // Récupérer l'option sélectionnée
  var selectedOption = selectElement.options[selectElement.selectedIndex];

  // Récupérer la valeur de l'option sélectionnée
  var selectedValue = selectedOption.value;

  // Vérifier si une option a été sélectionnée
  if (selectedValue === "") {
    document.getElementById('upload-status').innerText = 'Veuillez sélectionner une option.';
    return;
  }

  try {
    const response = await fetch('/charger', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ document: selectedValue })
    });


    if (response.ok) {
      document.getElementById('upload-status').innerText = 'Fichier chargé avec succès !';
    } else {
      document.getElementById('upload-status').innerText = 'Échec du chargement du fichier.';
    }
  } catch (error) {
    document.getElementById('upload-status').innerText = 'Une erreur est survenue lors du chargement.';
  }
};

document.getElementById('charger-doc').addEventListener('click', handleChargerClick);


audio.play();
