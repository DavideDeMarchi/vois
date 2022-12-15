.. image:: figures/vois_horizontal_small.png

|

.. _Vaas:

.. role:: raw-html(raw)
    :format: html
    
***************************************
Voilà as a Service in the BDAP platform
***************************************

The VaaS service is an automated deploy system that allows BDAP users to deploy their Voilà dashboards in production.
The deploy procedure runs every 15 minutes (at 0', 15', 30' and 45' minutes of every hour), to copy updated content from users' gitlab repositories to the production Voilà servers.

It has to be noted that the production Voilà servers have no connection to the BDAP storage systems (neither /eos nor /mnt/cidstorage are mounted), so that the only way to deploy an updated version of the dashboards is through the VaaS automated deploy procedure.

In the following figure, a schema of the dashboard development and deployment operation is shown: the development of the dashboards occurs inside the `JEO-lab service <https://jeodpp.jrc.ec.europa.eu/jhub/>`_, while the deployment in production is managed by VaaS using gitlab as code repository.

.. figure:: figures/Vaas.Final.small.png
   :scale: 100 %
   :alt: Component schema of dashboards development and deployment using VaaS
       
   Component schema of dashboards development and deployment using VaaS


The deployed dashboards listing will be visible through URLs like: https://jeodpp.jrc.ec.europa.eu/eu/vaas/voila/tree/<Root>/<Project>

The full procedure is explained by the following steps that will also define what are **Root** and **Project** names.

1. The deployment procedure starts from a **fork** operation (See `Gitlab documentation on fork <https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html>`_ ) of this template gitlab repository: https://jeodpp.jrc.ec.europa.eu/apps/gitlab/for-everyone/libraries/vaas/voila-notebook-template

    .. figure:: figures/fork.png
       :scale: 100 %
       :alt: Fork button in gitlab
       
       Voila notebook template and the **fork** button

    Users are invited to give a new name to the forked repository (**Project**): this name will be part of the path of the deployed dashboards.

    Any BDAP user can fork the template and create a copy of the repository into its private space (https://jeodpp.jrc.ec.europa.eu/apps/gitlab/<user-name>) or into the gitlab space of a use-case to which the user participates (https://jeodpp.jrc.ec.europa.eu/apps/gitlab/<use-case-name>).
    
:raw-html:`<br />`
2. The second step for deploying dashboards in the BDAP VaaS is to `create a gitlab issue under the original template gitlab repository <https://jeodpp.jrc.ec.europa.eu/apps/gitlab/for-everyone/support/-/issues/new?issuable_template=request_VoilaAsService>`_. This issue must contain the following information:

    1. **Root**: Root name where the project associated to this repo will be deployed.
    
        The dashboards will be visible under https://jeodpp.jrc.ec.europa.eu/eu/vaas/voila/render/<Root>/<Project>/<Dashboard>.ipynb. The **Root** name must be unique. It is recommended to use the name of the use-case to which the user belongs or the name of the JRC project for which the dashboard is developed in case the user is not linked to a BDAP use case, for example: **usecase1** or **JRCproject1**
    
    2. **Dashboard path**: full path of the **forked** copy of the template gitlab repository, for example: https://jeodpp.jrc.ec.europa.eu/apps/gitlab/usecase1/myvoilarepo

    3. **Description**: a brief description of the scope of the dashboards that will be deployed from the forked repo
    


3. At this point a manual operation, performed by members of the core BDAP team, will validate the information provided in the issue, for instance to check if the **Root** name is already existing, etc.. This operation ends with the approval of the new Voilà repo and the adding of the copy operation to the automated deploy procedure. The user will be informed of the success or failure of this check.
:raw-html:`<br />`

4. Upon successfull validation, the user can start to work on the development of its dashboards. The first operation is to access the JEO-lab service at https://jeodpp.jrc.ec.europa.eu/jhub/ and start the docker image called **"Interactive Processing - JupyterLab - Python 3"**, which is the first in the dropdown list. This is the docker image that contains all the libraries needed for the development of Voilà dashboards and it is the same image used by the Voilà servers. It is a "shared" docker image in the sense that all the deployed dashboards will use the same docker image. In case the user needs an additional python library, he/she should `open an issue in gitlab <https://jeodpp.jrc.ec.europa.eu/apps/gitlab/for-everyone/support/issues/new>`_ and ask for it. The request will be evaluated and possibly satisfied given that it is compatible with the dependencies and the already installed libraries.
:raw-html:`<br />`

5. After the launch of the JEO-lab docker image, the user should open a terminal window and navigate to a subfolder of its /home/<username> folder where a local copy of its Voilà repo should be created, and then execute a "git clone" command from the full path of its forked gitlab repo. Example::

    cd /home/myusername
    mkdir voila
    cd voila
    git clone https://jeodpp.jrc.ec.europa.eu/apps/gitlab/username/myvoilarepo.git
    
:raw-html:`<br />`
6. At this point the user can start to add content to the local copy of the repository, also using the JupyterLab interface to create and edit notebooks. There is a limit of 1GB on the amount of space that the repo can use. Inside this limit, the user can add to the repo subfolders, local CSV files, local vector datasets in **geojson** format, etc... User can then "git commit" and "git push" its content. After the push operation, the first deploy procedure execution will perform the copy of the full repo into the production Voilà servers, the updated dashboard will be published and a comment in the commit in Gitlab will notify you of the outcome of the deploy.

    Given that **Root** name is **usecase1**, and the forked **Project** name is **myvoilarepo**, this is the URL to view the list of all the deployed dashboards

    https://jeodpp.jrc.ec.europa.eu/eu/vaas/voila/tree/usecase1/myvoilarepo
    
    A notebook having name **dashboard1.ipynb** can be launched using this direct URL:
    
    https://jeodpp.jrc.ec.europa.eu/eu/vaas/voila/render/usecase1/myvoilarepo/dashboard1.ipynb
    

In the first phase of the VaaS service introduction, all the deployed dashboards will be visible to any EUlogin user with an email ending with **europa.eu**. In the near future we will work in allowing users to customise their deployment and decide which users can access their dashboards.

7. The VaaS server is isolated from any other BDAP resource, including the BDAP storage. If you need to access files from  the dashboard that are not suitable for a git repo (binary or large files), you can request that they are synchronized from the BDAP storage by indicating their location (one path per line, file or folder) in a `voila-data-location` file at the first level of your repository. The files will be synchronized when deploying the dashboard, not in realtime, so you need a commit to trigger their copy on the VaaS server.
   Maximum data size per dashboard : 10GB
