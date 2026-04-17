function checkPassword(password){

            // see checkName function and extend here .e.g. at least 8 character
            return false;
        }

        function checkName(name){

            var param_name = name; 
           // alert ("ParamName is " + param_name);

            //Write your own patterns here - this is just an example
            var pattern = /^[A-Za-z- ]+$/;

            //Apply pattern to name string - result will be false or true
            //alert(param_name.value);  //for testing
            var result = pattern.test(param_name);
            //alert (result);

            if (!result)
            {

                //alert('false');
                return false; 
                
            }            
            else 
            {
                //alert('true');
                return true;
            }
        }


        


        function formValidation(){

            var name = document.getElementById("uid").value;
            var password = document.getElementById("pw").value;

            var check = 0; 


            // only checking name you can extend this code to check email and password
            if (checkName(name)){                
                alert('Valid name and submitted');
                //return true; 

            }
            else
            {
                alert("Invalid name");
                document.MyForm.uid.focus();
                document.getElementById("uid").style.border='1px solid red';
                return false; 
            }     

            
            
            
            

            return false;  


        }