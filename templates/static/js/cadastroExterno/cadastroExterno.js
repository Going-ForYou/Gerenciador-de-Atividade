 document.addEventListener('DOMContentLoaded', function() {
            const beneficiaryDobInput = document.getElementById('beneficiaryDob');
            const guardianFields = document.getElementById('guardianFields');
            const beneficiaryForm = document.getElementById('beneficiaryForm');

            beneficiaryDobInput.addEventListener('change', function() {
                const dob = new Date(beneficiaryDobInput.value);
                const age = getAge(dob);
                if (age < 18) {
                    guardianFields.classList.remove('hidden');
                } else {
                    guardianFields.classList.add('hidden');
                }
            });

            function getAge(dob) {
                const diff = Date.now() - dob.getTime();
                const ageDate = new Date(diff);
                return Math.abs(ageDate.getUTCFullYear() - 1970);
            }

            beneficiaryForm.addEventListener('submit', function(event) {
                event.preventDefault();
                const formData = new FormData(beneficiaryForm);
                const data = {};
                formData.forEach((value, key) => {
                    data[key] = value;
                });
                console.log(data);
            });
        });