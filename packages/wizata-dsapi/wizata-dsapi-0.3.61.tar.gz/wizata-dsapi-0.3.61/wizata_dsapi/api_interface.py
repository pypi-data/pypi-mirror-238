import uuid
from .solution_component import SolutionComponent


class ApiInterface:
    """
    Interface with all methods available both to the pipeline runners and the Data Science API.
    """

    def get_components(self,
                       label_id: uuid.UUID = None,
                       twin_id: uuid.UUID = None,
                       template_id: uuid.UUID = None,
                       owner_id: uuid.UUID = None,
                       organization_only: bool = False,
                       name: str = None):
        """
        get components
        :param label_id: filter on a specific label
        :param template_id: filter on a specific template
        :param twin_id: filter on a specific twin
        :param owner_id: filter on a specific owner_id
        :param organization_only: work only with organization components (by default - False)
        :param name: filter on a specific name (contains)
        """
        pass

    def create_component(self, component: SolutionComponent):
        """
        create a component based on its ID.
        """
        pass

    def update_component(self, component: SolutionComponent):
        """
        update a component based on its ID.
        """
        pass

    def delete_component(self, component_id: uuid.UUID):
        """
        delete component
        """
        pass

    def get_business_labels(self) -> dict:
        """
        get a name / uuid dictionary with all business labels in platform.
        """
        pass

    def get_datapoint_mappings(self, registration):
        """
        get datapoint mapping from a registration.
        """
        pass

    def get_registrations(self, template) -> list:
        """
        retrieve all registrations for
        :param template: template object, UUID or str key.
        :return: list of twin registration.
        """
        pass
