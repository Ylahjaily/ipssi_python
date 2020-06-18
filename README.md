
<h3>Instalation</h3>
   <ul>
        <li>git clone https://github.com/Ylahjaily</li>
        <li>docker-compose up</li>
    </ul>
<h3>Initialization</h3>
<ul>
    <li> Open Portainer running at http://localhost:30033/ </li>
    <li> Open the Ipssi-python container's console </li>
<ul>    
        <ul>
        <li>pip-install -r requirements.txt</li>
        <li>python manage.py makemigrations</li>
        <li>pyhton manage.py migrate</li>
        <li>python manage.py runserver 0:8000</li>
        <li>python manage.py createsuperuser</li>
        </ul>


