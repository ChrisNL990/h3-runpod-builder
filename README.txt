REMOTE H3 RUNPOD BUILD — no Docker installation on your PC

This is generic launcher code only. It contains NO workflow prompts, input
filenames, Hugging Face token, private setup ZIP, or model weights.
Your H3_RunPod_Setup.zip stays in your existing private Hugging Face repository.
The new image replaces the fixed entrypoint, which ignored RunPod's CMD override.

1. Create a GitHub repository named h3-runpod-builder. Upload the CONTENTS of
   this folder to its root (Dockerfile and bootstrap.py must be at the root).
   A public repository is suitable for these generic files, if you choose it.
   Do not upload your private H3_RunPod_Setup.zip or credentials to GitHub.
2. Ensure .github/workflows/build.yml exists. If browser upload skips that hidden
   folder: Add file > Create new file; name it .github/workflows/build.yml; paste
   the contents of the included build.yml and commit. The .dockerignore is helpful
   but not required: Dockerfile copies ONLY bootstrap.py into the image.
3. Open Actions > Build H3 RunPod image > Run workflow. This uses a GitHub-hosted
   CPU runner, not your RunPod GPU. No HF token is needed during the build.
4. After success, the job summary shows ghcr.io/YOUR_USERNAME/h3-runpod:COMMIT.
   New GitHub container packages default to private. You can keep the image private
   and add registry credentials in RunPod, or make ONLY this generic image public
   through your GitHub profile > Packages > h3-runpod > Package settings > visibility.
   Making it public does not expose your private workflow ZIP or runtime token.
5. Edit your private RunPod template:
   - Container image: the image from the successful job summary (commit tag).
   - DELETE the old Container Start Command. New image owns startup.
   - Keep COMFYUI_VENV_NAME=.venv-cu132, HF_TOKEN as RunPod secret,
     H3_SETUP_URL pointing to your private ZIP, and JUPYTER_PASSWORD as a secret.
   - Keep ports 8188/8888 HTTP and your chosen disposable disk size.
   - Registry auth stays empty ONLY if you made the generic image public.
6. Test a new pod. Expect private-ZIP download -> base startup -> H3 provisioning
   -> models validated -> ComfyUI READY. No manual downloader should run alongside.

The remote job pulls the large base SOFTWARE image, then pushes the derived
image layers to GitHub. It never downloads or uploads the model weights.
GitHub build/storage allowances depend on your plan and repository visibility;
check any billing prompt before enabling paid usage. No fresh GPU test has been
performed. The workflow checks Python syntax, the entrypoint and the base hook
marker; it does not test CUDA generation. Never run with shell tracing (set -x),
which could log credentials. Failure logs should be reviewed before sharing.
