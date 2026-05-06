import time


class SettingsStore:
    def __init__(self, settings):
        self.settings = settings

    # --- AGE GROUP ---
    def find_ag(self, ag_id):
        return next(
            (x for x in self.settings.get("age_groups", []) if x["id"] == ag_id), None
        )

    def get_age_groups(self):
        return self.settings.get("age_groups", [])

    def add_age_group(self, name="Жаңа топ"):
        new_item = {"id": f"ag_{time.time_ns()}", "name": name, "domains": []}
        if "age_groups" not in self.settings:
            self.settings["age_groups"] = []
        self.settings["age_groups"].append(new_item)
        return new_item

    def update_age_group(self, ag_id, new_name):
        ag = next((x for x in self.settings["age_groups"] if x["id"] == ag_id), None)
        if ag:
            ag["name"] = new_name
            return True
        return False

    def delete_age_group(self, ag_id):
        self.settings["age_groups"] = [
            ag for ag in self.settings["age_groups"] if ag["id"] != ag_id
        ]

    # --- DOMAIN ---

    def find_dom(self, ag_id, dom_id):
        ag = self.find_ag(ag_id)
        if ag:
            return next((x for x in ag["domains"] if x["id"] == dom_id), None)
        return None

    def get_domains(self, age_group_idx):
        try:
            return self.settings["age_groups"][age_group_idx]["domains"]
        except (IndexError, KeyError):
            return []

    def add_domain(self, ag_id, name="Жаңа бағыт"):
        ag = self.find_ag(ag_id)
        if ag:
            new_dom = {"id": f"dom_{time.time_ns()}", "name": name, "subjects": []}
            ag["domains"].append(new_dom)
            return new_dom
        return None

    def delete_domain(self, ag_id, dom_id):
        ag = self.find_ag(ag_id)
        if not ag:
            return
        ag["domains"] = [dom for dom in ag["domains"] if dom["id"] != dom_id]

    # --- SUBJECT ---

    def find_sub(self, ag_id, dom_id, sub_id):
        dom = self.find_dom(ag_id, dom_id)
        if dom:
            return next((x for x in dom["subjects"] if x["id"] == sub_id), None)
        return None

    def get_subjects(self, ag_idx, dom_idx):
        try:
            return self.settings["age_groups"][ag_idx]["domains"][dom_idx]["subjects"]
        except (IndexError, KeyError):
            return []

    def add_subject(self, ag_id, dom_id, name="Жаңа пән"):
        dom = self.find_dom(ag_id, dom_id)
        if dom:
            new_sub = {"id": f"sub_{time.time_ns()}", "name": name, "metrics": []}
            dom["subjects"].append(new_sub)
            return new_sub
        return None

    def delete_subject(self, ag_id, dom_id, sub_id):
        dom = self.find_dom(ag_id, dom_id)
        if not dom:
            return
        dom["subjects"] = [sub for sub in dom["subjects"] if sub["id"] != sub_id]

    # --- METRIC ---

    def add_metric(self, ag_id, dom_id, sub_id, code_prefix):
        sub = self.find_sub(ag_id, dom_id, sub_id)
        if sub:
            new_met = {
                "id": f"metric_{time.time_ns()}",
                "code": f"{code_prefix}.{len(sub['metrics']) + 1}",
                "transformed": "",
                "criteria": ["", "", ""],
            }
            sub["metrics"].append(new_met)
            return new_met
        return None

    def delete_metric(self, ag_id, dom_id, sub_id, met_id):
        sub = self.find_sub(ag_id, dom_id, sub_id)
        if not sub:
            return
        sub["metrics"] = [met for met in sub["metrics"] if met["id"] != met_id]
