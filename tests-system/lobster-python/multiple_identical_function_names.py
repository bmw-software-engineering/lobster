#

flag = False
requirements_global = None

if flag:
    def get_requirements(requirements):
        return requirements
else:
    def set_requirements(requirements):
        requirements_global = requirements
        return requirements_global


def get_requirements(requirements):
    return requirements


def display_requirements():
    print(get_requirements())


def set_requirements(requirements):
    requirements_global = requirements
    return requirements_global


def get_requirements(requirements):
    return requirements
