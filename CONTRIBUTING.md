# Cómo contribuír con el proyecto
=================================

1. Haga un Fork del proyecto en github. [1]
    * Vaya al repositorio [https://github.com/bvsf/sigcaw](https://github.com/bvsf/sigcaw).
    * En la esquina superior derecha haga clic en Fork. ![Fork](https://help.github.com/assets/images/help/repository/fork_button.jpg)
2. Clone en su PC el proyecto Forkeado en su cuenta [2][3].
    * Vuelva a su perfil de GitHub.
    * Busque entre sus proyectos el que acaba de Forkear (sigcaw).
    * Haga clic en el botón **Clone or Download**. ![Clone](https://help.github.com/assets/images/help/repository/clone-repo-clone-url-button.png)
    * Copie la url.
    * En su computadora, usando la Terminal de comandos, cree un directorio de trabajo.
    * En dicho directorio ejecute el siguiente comando *git clone* y peque la url copiada.
      
         ```
         git clone https://la-url-que-copio-del-botón-clone
         ```
         
    * Ese comando creará un directorio con el proyecto y descargará en él lo que se ha Forkeado.
    * Ahora puede verificar los *remote* de su projecto con el comando
        ```git remote -v```
    * Obtendrá un listado similar al siguiente:
      
        ```
        origin	https://la-url-que-copio-del-botón-clone (fetch)
        origin	https://la-url-que-copio-del-botón-clone (push)
        ```
        
    * Para que Ud. pueda luego sincronizar su proyecto (Fork) con el proyecto original debe agregar un *remote* que apunte al proyecto original
      
        ```
        git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git
        ```
        
    * Si vuelve a verificar los *remote* de su proyecto verá agregado dos nuevos ítems, algo similar a lo siguiente:
      
        ```
        origin	https://la-url-que-copio-del-botón-clone (fetch)
        origin	https://la-url-que-copio-del-botón-clone (push)
        upstream	https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git (fetch)
        upstream	https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git (push)
        ```
    
3. Trabaje en un Issue del proyecto original en su propia copia del proyecto
    * Siempre trabajaremos con al menos tres branchs, **master**, **develop** y **feature/issueN** (que explicamos a continuación).
    * Puede ver las ramas de su repositorio actual haciendo
      
        ```
        git branch
        ```
        
      nota:puede que luego de clonar el repositorio no vea todas las ramas del fork en su PC sino solamente la rama **master** en este caso deberá crear las ramas faltantes pero tomando la rama desde el fork origen. Por ejemplo si debemos crear la rama **develop** tomando como base la rama del fork:
      
        ```
        git checkout -b develop origin/develop
        ```
         
    * Posicionese en el branch **develop** (o la que ud. crea conveniente) para crear a partir de ella una nueva branch.
      
        ```
        git checkout develop
        ```
         
    * Crear una branch en su PC que se llame **feature/issueN** (donde N es el numero del issue que se le asignó para trabajar).
    * Para crear un nuevo branch se usa el comando:
      
        ```
        git checkout -b nombre_del_branch
        ```
        
    * Git lo lleva inmediatamente al branch creado, en él comience a trabajar.
    * Con el comando ```git status``` puede listar los archivos que sufrieron modificaciones.
    * Con el comand ```git add nombre_del_archivo``` puede pasar los archivos modificados que ud. desee a la zona de *Stage*
    * Cuando termine de modificar un archivo, es recomendable, luego de pasarlo a la zona de Stage, que lo comitee indicando un texto descriptivo con
      
        ```
        git commit -m "Algún texto descriptivo de lo que hizo"
        ```
        
    * Se recomienda que los commit sean lo más *atómicos* que ud. considere posible, ya que ante una mala decisión estos son los puntos a los que puede volver atrás a corregir su error (una forma análoga a los checkpoints de los videojuegos).
4. Suba los cambios de su PC a su proyecto Forkeado [4]
    * Una vez que ha terminado de corregir y probar el Issue asignado a ud. deberá subir su rama a github.com:
    * Suba la rama **feature/issueN** a github.com (master no debería tener cambios ya que se usa pura y exclusivamente para el código en producción, y combinar a la rama develop luego complica el pull request al proyecto original, sobre todo cuando se trabajan con varios pull request en simultáneo).
      
        ```
        git push origin feature/issueN
        ```
         
5. Haga un Pull Request al proyecto original [5]
    * Desde la pagina de github.com realize un **Pull Request** desde la rama **feature/issueN** a la rama **develop** del proyecto original
    * Posiciónese, en github.com en la branch **feature/issueN** ![Branch](https://help.github.com/assets/images/help/branch/pick-your-branch.png)
    * Haga clic en el botón *New Pull Request* ![New Pull Request](https://help.github.com/assets/images/help/pull_requests/pull-request-start-review-button.png)
    * Complete toda la información necesaria (recuerde elegir la rama *develop* en el proyecto original) y una vez seguro de los cambios presione el botón de *Create Pull Request*  ![Create Pull Request](https://help.github.com/assets/images/help/pull_requests/pull-request-review-create.png)
    * La explicación es aún más larga, recomendamos encarecidamente que lea el enlace que la ayuda de github.com proporciona [6]]
6. Sincronize su proyecto Forkeado desde el original [6]
    * Al trabajar en equipos puede que el proyecto original cambie por otros miembros y ud. deber tener que descargar esa información a su PC para poder trabajar siempre con las ultimas versiones disponibles para evitar desfazajes muy amplios, para ello debe sincronizar el repositorio original con el de su PC, para ello ejecute el comando:
      
        ```
        git fetch upstream
        ```
         
    * Git descargará en su pc el repositorio remoto, sus branchs y commits. Los branchs se llamaran algo similara a "upstream/develop" Ud. deberá unir esta branch con la propia branch develop de su Pc (y de forma análoga con master, etc.) con los comandos:
      
        ```
        git checkout develop
        git merge upstream/develop
        ```
        
7. Vuelva al punto 3


## Bibliografía

* [1] [https://help.github.com/articles/fork-a-repo/](https://help.github.com/articles/fork-a-repo/)
* [2] [https://help.github.com/articles/cloning-a-repository/](https://help.github.com/articles/cloning-a-repository/)
* [3] [https://help.github.com/articles/configuring-a-remote-for-a-fork/](https://help.github.com/articles/configuring-a-remote-for-a-fork/)
* [4] [https://help.github.com/articles/pushing-to-a-remote/](https://help.github.com/articles/pushing-to-a-remote/)
* [5] [https://help.github.com/articles/using-pull-requests/](https://help.github.com/articles/using-pull-requests/)
* [6] [https://help.github.com/articles/syncing-a-fork/](https://help.github.com/articles/syncing-a-fork/)
* [https://git-scm.com/book/ch5-2.html](https://git-scm.com/book/ch5-2.html)
* [https://help.github.com/categories/collaborating-on-projects-using-issues-and-pull-requests/](https://help.github.com/categories/collaborating-on-projects-using-issues-and-pull-requests/)
* [http://rogerdudler.github.io/git-guide/index.es.html](http://rogerdudler.github.io/git-guide/index.es.html
