import os
import tqdm
import pandas as pd
import shutil

base_dir = "."
branch = "dev"
checking_dependency = "log4j-core"
base_ssh_url = "github.com:DaniilRoman"
project_list = ["a_tinder_like_app ", "design_patterns_course"]


if __name__ == '__main__':
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    os.chdir(base_dir)

    components_with_dep = []
    components_without_dep = []
    filtered_projects = []
    for project in tqdm.tqdm(project_list):
        project_dir = os.path.join(base_dir, project)
        try:
            os.system(f"git clone --branch {branch} git@{base_ssh_url}/{project}.git")
            if not os.path.exists(project_dir):
                os.system(f"git clone git@{base_ssh_url}/{project}.git")

            try:
                os.chdir(project_dir)

                if not os.path.exists(os.path.join(project_dir, "pom.xml")):
                    print(f"Not java project: {project}")
                    filtered_projects.append(project)
                    continue

                deps = os.popen(f"mvn dependency:tree | grep {checking_dependency}").read()
                exists = deps is not None and checking_dependency in deps
                if exists:
                    components_with_dep.append([project, deps])
                else:
                    components_without_dep.append([project, deps])

            except:
                filtered_projects.append(project)
                print(f"Error with {project}")
            finally:
                os.chdir(base_dir)

        except:
            filtered_projects.append(project)
            print(f"Error cloning with {project}")
        finally:
            if os.path.exists(project_dir):
                shutil.rmtree(project_dir)

    components_with_dep_df = pd.DataFrame(components_with_dep, columns=['Component', 'Output'])
    components_with_dep_df.to_csv(os.path.join(base_dir, "result_with_deps.csv"))

    components_without_dep_df = pd.DataFrame(components_without_dep, columns=['Component', 'Output'])
    components_without_dep_df.to_csv(os.path.join(base_dir, "result_without_deps.csv"))

    filtered_projects = list(dict.fromkeys(filtered_projects))
    filtered_projects_df = pd.DataFrame(filtered_projects, columns=['Project'])
    filtered_projects_df.to_csv(os.path.join(base_dir, "filtered_projects.csv"))

