# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # import subprocess
# # import logging

# # app = Flask(__name__)
# # # Configure CORS to allow specific origins (or set it to "*")
# # CORS(app, resources={r"/transcribe": {"origins": "*"}})

# # # Configure logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)


# # @app.route("/transcribe", methods=["POST"])
# # def transcribe():
# #     data = request.json
# #     url = data.get("url")
# #     model = data.get("model", "large")
# #     language = data.get("language", "en")
# #     use_whisper_api = data.get("use_whisper_api", False)
# #     openai_api_key = data.get("openai_api_key", "")
# #     gpt_translation_prompt = data.get("gpt_translation_prompt", "")
# #     google_api_key = data.get("google_api_key", "")

# #     command = ["stream-translator-gpt", url, "--model", model, "--language", language]

# #     # Add Whisper API key if enabled
# #     if use_whisper_api:
# #         if not openai_api_key:
# #             return jsonify({"error": "Missing OpenAI API Key for Whisper API"}), 400
# #         command.extend(["--use_whisper_api", "--openai_api_key", openai_api_key])
# #     else:
# #         # Use Faster Whisper if Whisper API is not enabled
# #         command.append("--use_faster_whisper")

# #     # Add GPT translation prompt
# #     if gpt_translation_prompt:
# #         command.extend(["--gpt_translation_prompt", gpt_translation_prompt])

# #     # Add Google API key if provided
# #     if google_api_key:
# #         command.extend(["--google_api_key", google_api_key])

# #     logger.info(f"Running command: {' '.join(command)}")

# #     try:
# #         # Execute the command and capture the result
# #         result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
# #         logger.info(f"Command output: {result}")
# #         return jsonify({"result": result})
# #     except subprocess.CalledProcessError as e:
# #         logger.error(f"Error executing command: {str(e)}")
# #         logger.error(f"Command output: {e.output}")
# #         return jsonify({"error": str(e), "output": e.output}), 400


# # if __name__ == "__main__":
# #     app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import subprocess
# import logging
# import yt_dlp

# app = Flask(__name__)
# # Configure CORS to allow specific origins (or set it to "*")
# CORS(app, resources={r"/transcribe": {"origins": "*"}})

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# def get_video_duration(url):
#     """
#     Get video duration using yt-dlp.
#     Args:
#         url (str): YouTube video URL.
#     Returns:
#         int: Duration of the video in seconds.
#     """
#     try:
#         ydl_opts = {
#             "quiet": True,
#             "no_warnings": True,
#             "format": "best",
#             "simulate": True,
#             "skip_download": True,
#             "force_generic_extractor": True,
#         }
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             return info_dict.get("duration", None)
#     except Exception as e:
#         logger.error(f"Error retrieving video duration: {str(e)}")
#         return None


# @app.route("/transcribe", methods=["POST"])
# def transcribe():
#     data = request.json
#     url = data.get("url")
#     model = data.get("model", "large")
#     language = data.get("language", "en")
#     use_whisper_api = data.get("use_whisper_api", False)
#     openai_api_key = data.get("openai_api_key", "")
#     gpt_translation_prompt = data.get("gpt_translation_prompt", "")
#     google_api_key = data.get("google_api_key", "")

#     command = ["stream-translator-gpt", url, "--model", model, "--language", language]

#     # Add Whisper API key if enabled
#     if use_whisper_api:
#         if not openai_api_key:
#             return jsonify({"error": "Missing OpenAI API Key for Whisper API"}), 400
#         command.extend(["--use_whisper_api", "--openai_api_key", openai_api_key])
#     else:
#         # Use Faster Whisper if Whisper API is not enabled
#         command.append("--use_faster_whisper")

#     # Add GPT translation prompt
#     if gpt_translation_prompt:
#         command.extend(["--gpt_translation_prompt", gpt_translation_prompt])

#     # Add Google API key if provided
#     if google_api_key:
#         command.extend(["--google_api_key", google_api_key])

#     logger.info(f"Running command: {' '.join(command)}")

#     # Get the expected video duration
#     video_duration = get_video_duration(url)
#     if video_duration is None:
#         return jsonify({"error": "Could not retrieve video duration"}), 400

#     try:
#         # Execute the command and capture the result
#         result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
#         logger.info(f"Command output: {result}")

#         # Check if the transcription is complete
#         processed_duration = None
#         for line in result.splitlines():
#             if "processed duration:" in line:
#                 processed_duration_str = line.split("processed duration:")[-1].split()[
#                     0
#                 ]
#                 processed_duration = int(float(processed_duration_str))
#                 break

#         if processed_duration is not None and processed_duration < video_duration:
#             logger.warning(
#                 f"Processed duration ({processed_duration}s) is less than video duration ({video_duration}s)"
#             )
#             return jsonify({"error": "Transcription incomplete", "output": result}), 400

#         return jsonify({"result": result})
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Error executing command: {str(e)}")
#         logger.error(f"Command output: {e.output}")
#         return jsonify({"error": str(e), "output": e.output}), 400


# if __name__ == "__main__":
#     app.run(debug=True)
