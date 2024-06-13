
    document.getElementById('beneficiaryDob').addEventListener('change', function() {
        const dob = new Date(this.value);
        const age = getAge(dob);
        if (age < 18) {
            document.getElementById('guardianFields').classList.remove('hidden');
        } else {
            document.getElementById('guardianFields').classList.add('hidden');
        }
    });

    function getAge(dob) {
        const diff = Date.now() - dob.getTime();
        const ageDate = new Date(diff);
        return Math.abs(ageDate.getUTCFullYear() - 1970);
    }

    document.getElementById('saveChangesBtn').addEventListener('click', function() {
        document.getElementById('saveConfirmation').style.display = 'block';
    });

    document.getElementById('confirmSaveBtn').addEventListener('click', function() {
        saveChanges();
        document.getElementById('saveConfirmation').style.display = 'none';
    });

    document.getElementById('cancelSaveBtn').addEventListener('click', function() {
        document.getElementById('saveConfirmation').style.display = 'none';
    });

    function saveChanges() {
        const formData = new FormData(document.getElementById('beneficiaryForm'));
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        console.log(data);
        showNotification('Alterações salvas com sucesso!');
    }

    function showNotification(message) {
        const notification = document.getElementById('notification');
        notification.innerText = message;
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 3000);
    }
