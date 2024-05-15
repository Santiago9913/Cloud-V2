terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.29.0"
    }
  }
}

provider "google" {
  project = "cloud-dev-421516"
}

resource "google_storage_bucket" "videos_dev_cloud_v2" {
  name                     = "videos_dev_cloud_v2"
  location                 = "US"
  force_destroy            = true
  public_access_prevention = "enforced"
}

resource "google_storage_bucket" "worker_bucket" {
  name                        = "worker_bucket"
  location                    = "US"
  force_destroy               = true
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "worker_zip" {
  name   = "worker.zip"
  bucket = google_storage_bucket.worker_bucket.name
  source = "./worker.zip"
}

resource "google_pubsub_topic" "process_video_v2" {
  name = "process_video_v2"
}

resource "google_artifact_registry_repository" "video_processor_v2" {
  repository_id = "video-processor-v2"
  location      = "us-central1"
  format        = "DOCKER"
}

resource "google_cloudfunctions2_function" "worker" {
  depends_on  = [google_storage_bucket_object.worker_zip, google_artifact_registry_repository.video_processor_v2, google_pubsub_topic.process_video_v2]
  name        = "worker-v2"
  location    = "us-central1"
  description = "Worker function to process video from Terraform"
  build_config {
    runtime               = "python311"
    entry_point           = "process_video"
    source {
      storage_source {
        bucket = google_storage_bucket.worker_bucket.name
        object = google_storage_bucket_object.worker_zip.name
      }
    }
  }

  service_config {
    max_instance_count               = 2
    min_instance_count               = 0
    available_memory                 = "2Gi"
    timeout_seconds                  = 60
    max_instance_request_concurrency = 10
    available_cpu                    = 1
    ingress_settings                 = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision   = true
  }

  event_trigger {
    trigger_region = "us-central1"
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.process_video_v2.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}





