from banana_dev import API

api = API("11111111-1111-1111-1111-111111111111")
projects, status = api.listProjects()
print('list',projects,status)

project, status = api.getProject(projects["results"][0]["id"])
print('get',project,status)

updatedProject, status = api.updateProject(projects["results"][0]["id"], {"maxReplicas": 2})
print('update',updatedProject,status)
