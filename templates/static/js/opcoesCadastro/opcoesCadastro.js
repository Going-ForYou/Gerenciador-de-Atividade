 function toggleDropdown(event, dropdownId) {
        event.preventDefault();
        var dropdown = document.getElementById(dropdownId);
        dropdown.style.display = dropdown.style.display === 'none' || dropdown.style.display === '' ? 'block' : 'none';
    }

    // Simulação de carregamento de dados do usuário
    document.addEventListener("DOMContentLoaded", function() {
        // Exemplo de dados do usuário, que seriam carregados dinamicamente
        var userProfile = {
            name: "Samuel",
            picture: "D:/DocumentosHD/PROJETO WEB3/img/perfil.jpg" // Caminho da imagem
        };

        document.getElementById("profile-name").textContent = userProfile.name;
        document.getElementById("profile-picture").src = userProfile.picture;
    });

    document.addEventListener('DOMContentLoaded', function() {
        // Modal
        var modal = document.getElementById("myModal");
        var modalIframe = document.getElementById("modalIframe");
        var modalLinks = document.querySelectorAll(".modal-link");
        var closeModal = document.getElementsByClassName("close")[0];

        modalLinks.forEach(function(link) {
            link.onclick = function(event) {
                event.preventDefault();
                modalIframe.src = link.getAttribute("data-url");
                modal.style.display = "block";
            }
        });

        closeModal.onclick = function() {
            modal.style.display = "none";
            modalIframe.src = ""; 
        }

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
                modalIframe.src = "";
            }
        }
    });