from locust import (
    HttpUser,
    task,
    between
)


class QueryUser(HttpUser):

    wait_time = between(1, 3)

    @task(7)
    def query_pipeline(self):

        self.client.get(
            "/health"
        )


class IngestUser(HttpUser):

    wait_time = between(2, 5)

    @task(2)
    def ingest_document(self):

        self.client.get(
            "/health"
        )


class AdminUser(HttpUser):

    wait_time = between(3, 6)

    @task(1)
    def check_evaluations(self):

        self.client.get(
            "/health"
        )