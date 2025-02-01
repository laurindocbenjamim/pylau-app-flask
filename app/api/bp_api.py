

import os
from flask import Blueprint

from datetime import datetime
from app.dependencies import Api
from app.dependencies import request, current_app, jsonify, cross_origin
from app.api.upload_factory.file_upload import save_uploaded_file 
from flask import session

from app.api.video_store.video_resource import VideoResource
from app.api.video_analyzer.video_analyzer import VideoAnalyzerResource
from app.api.upload_factory.cv_customizer import CvCustomizerResource
from app.api.upload_factory.upload_multiple_controller import FilesUploadResource
from app.api.video_store.video_files_resource import VideoFilesResource
from app.api.market.stock_resource import StockResource
from app.api.market.cryptocurrency_resource import CryptoCurrencyResource
from app.api.storage.storage_resource import StorageResources
from app.api.storage.download_docs_resource import DownloadDocsResources

from app.api.csrf_token import CSRFToken
from app.configs_package import csrf
from app.models.extract_files_content import ExtractorFileContent
from app.models.pdf_reader_factory import PdfReaderFactory
from app.models.openai_api import OpenAiApi
from app.package_prompts.cv_customiser_prompts import CvPrompts
from app.models.docx_factory import DocxFileFactory

bp_api = Blueprint('api', __name__, url_prefix='/api')

api = Api(bp_api)#API  

api.add_resource(CSRFToken, '/csrf-token/get')

api.add_resource(VideoResource, '/files-storage/video/get/<string:filename>')
api.add_resource(VideoFilesResource, '/files-storage/video/list/<string:directory>')

# Add resource endpoints 
api.add_resource(CvCustomizerResource, '/upload')
api.add_resource(DownloadDocsResources, '/files-storage/download/<string:filename>')
api.add_resource(FilesUploadResource, '/files-storage/upload')

# Create the Video analyzer API endpoint
api.add_resource(VideoAnalyzerResource, '/video-analyzer/demo')

api.add_resource(StockResource,'/stocks')
api.add_resource(CryptoCurrencyResource, '/crypto')

api.add_resource(StorageResources, '/storage/request/<string:filename>')


from .netcaixa import bp_netcaixa_api
bp_api.register_blueprint(bp_netcaixa_api)


from app.api.storage.file_download_api_view import FileDownloadResource
# Register API endpoint
download_path=os.path.join('app', 'static', 'uploads', 'docs')
file_view = FileDownloadResource.as_view('file_api')

bp_api.add_url_rule(
    '/files-storage/doc/download/<string:filename>',
    view_func=file_view,
    methods=['GET']
)

# Customize CV
def cv_customizer_with_chat_gpt(*, client_cv, job_requirement):
    if not client_cv:
        return False, "The client cv content is required."
    elif not job_requirement:
        return False, "The Job requirements is required"

    prompt=CvPrompts()
    try:
        cv_optimization_prompt=prompt.get(job_description=job_requirement, cv_content=client_cv, id=1)
        optimise=cv_optimization_prompt.format(
                            job_description=job_requirement,
                            cv_content=client_cv
                        )
        openai_api = OpenAiApi()
        status, response=openai_api.request_with_model_4(prompt=optimise)
        return True, response
    except Exception as e:
        return False, str(e)

@bp_api.route('/cv-customizer', methods=['POST'])
@cross_origin(methods=['POST'])
@csrf.exempt
def cv_customizer():
    csrf_token = request.headers.get('X-Csrf-Token')
    """try:
        # Convert request headers to a dictionary
        headers_dict = dict(request.headers)

        # Convert the dictionary to a JSON string
        headers_json = json.dumps(headers_dict, indent=4)
        # Use the JSON string in your log message
        log_message = f"Headers: {headers_json}"
        current_app.logger.debug(f"Headers: {log_message}, CSRF-TOKEN: {csrf_token}")

        if not csrf_token:
            raise ValueError("CSRF token is missing")
        
        validate_csrf(csrf_token)
    except Exception as e:
        return jsonify({"status":403, "error": f"Invalid CSRF token: {str(e)}", "csrf-token-received":csrf_token})
    """
  
  
    # Check if the request contains the file part
    if 'contentOrigin' in request.form and request.form['contentOrigin'] =='file':
        if 'cvUpload' not in request.files:
            return jsonify({"status":400, "error": "No file part"})
        elif 'jobRequirements' not in request.files:
            return jsonify({"status":400, "error": "No file part"})

        file = request.files['cvUpload']
        file2 = request.files['jobRequirements']
        
        # Check if a file has been selected
        if file.filename == '' or file2.filename == '':
            return jsonify({"status":400, "error": "No selected file"})

        # Use the save_uploaded_file function from the module
        
        filepath=os.path.join(current_app.root_path, 'static', current_app.config['UPLOAD_FOLDER'])
        status,result = save_uploaded_file(file,filepath)

        files_path={}
        if not status:
            return jsonify({"status":400, "error": f"Filed to customize the CV. {result['error']}!"})
        else:
            files_path['cv_client']=result['file_path']
            status,result = save_uploaded_file(file2,filepath)
            files_path['job_requirements_file']=result['file_path'] if status else result
            
            pdf_reader=PdfReaderFactory()

            # Extract content from files and remove them
            files_path['cv_client_content']=pdf_reader.extract_text_fitz(files_path['cv_client'])
            if os.path.exists(files_path['cv_client']):
                os.remove(files_path['cv_client'])                
            
            files_path['job_requirement_content']= pdf_reader.extract_text_fitz(files_path['job_requirements_file'])

            # Reove the file
            if os.path.exists(files_path['job_requirements_file']):
                os.remove(files_path['job_requirements_file'])
                
            # Request  the customization to ChatGPT
            status, optimized_cv = cv_customizer_with_chat_gpt(client_cv=files_path['cv_client_content'],
            job_requirement=files_path['job_requirement_content'])

            if 'error' in optimized_cv or '404' in  optimized_cv:
                return jsonify({"status":404, "error": f"IA assistant Failed to customise the CV. {str(optimized_cv)}"})
            
            # Save the content created to docx
            docx=DocxFileFactory()
            
            session['DOWNLOAD_PATH']=filepath
            #docx.save_to_docx(content=optimized_cv, filepath=filepath, filename="customised_cv.docx")
            # Save to temporary file
            if not status:
                return jsonify({"status":404, "error": f"CV optimisation failed. {str(optimized_cv)}"})
            
            try:
                if not optimized_cv or optimized_cv=='':
                    return jsonify({"status":404, "error": f"Null CV optimisation. {str(optimized_cv)}"})
                                
                file_name=os.path.join(filepath,"optimized_cv.md")
                with open(file_name, "w") as f:
                    f.write(optimized_cv)
                    
                doc_filename=f'cv_optimised_{datetime.now().strftime('%Y%m%d%H%M%S')}'
                pdf_filename=f'{doc_filename}.pdf'
                new_file_path=docx.save_as_docx(optimized_cv=optimized_cv,file_path=filepath, filename=doc_filename)            

                res=docx.docx_to_pdf(docx_path=new_file_path, pdf_path=os.path.join(filepath,pdf_filename))
                
                
                return jsonify({"status": 200, "message": "Your CV was optimised successfully!", 
                                "docx_file_path": f'api/files-storage/doc/download/{doc_filename}.docx',
                                "pdf_file_path": f'api/files-storage/doc/download/{pdf_filename}'}), 200
            except Exception as e:
                return jsonify({"status":400, "error": f"Failed to optimise the CV! {str(e)}"})
    else: 
        return jsonify({"status":404, "error": "The origin field has not been found!"})