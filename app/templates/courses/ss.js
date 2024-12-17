newObjective.innerHTML = `
          <form id="courseForm" class="courseForm" novalidate enctype="multipart/form-data">
                <div class="row g-1" id="courseContentContainer01">

                  <div class="col-12">
                    <div class="input-group">
                    <input type="text" id="course_module" name="course_module" class="form-control mb-2"
                placeholder="Course module" >
          
                              <div class="invalid-feedback">
                                Your course's module is required.
                              </div>
                              </div>
                  </div>

                  <!-------->
                  <div class="col-12" id="content-module"></div>
                  <!-------->
                  <div class="col-12">
                    <div class="input-group has-validation">
                      <input type="text" id="course_topic" name="course_topic" class="form-control mb-2"
                        placeholder="Topic" required>
                      <div class="invalid-feedback">
                        Your course's topic is required.
                      </div>
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="input-group has-validation" id="">
                      <input type="radio" class="btn-check option5" value="localhost" name="course_content_origin" id="option5"
                        autocomplete="off" checked>
                      <label class="btn btn-outline-success" for="option5">Local host</label>

                      <input type="radio" class="btn-check option6" value="youtube" name="course_content_origin" id="option6"
                        autocomplete="off">
                      <label class="btn btn-outline-success" for="option6">Youtube</label>

                      <div class="invalid-feedback">
                        Your content origin is required.
                      </div>
                    </div>
                  </div>

                  <div class="col-12">
                    <div class="input-group has-validation">
                      <input type="file" id="videoFile" name="video" accept="video/*" class="form-control mb-2"
                        placeholder="Develope fix problems skills" required>
                      <div class="invalid-feedback">
                        Your video file is required.
                      </div>
                    </div>
                  </div>

                </div>

                <div class="my-3" id="error-block">
                  <div class="progress loading" role="progressbar" aria-label="Info striped example" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar progress-bar-striped bg-info" style="width: 50%"></div>
</div>
                 
                  <div class="error-message" style="display: none;"></div>
                  <div class="sent-message" style="display: none;">Your message has been sent. Thank you!</div>
                </div>

                <!-- Submit Button -->
                <div class="text-left">
                  <button type="submit" id="btn-save" class="btn btn-light btn-large btn-save">
                    <i class="fas fa-save"></i> Save Course
                  </button>
                </div>
              </form>
        `;

      // Add remove event to the button
      newObjective.querySelector(".option5").addEventListener("click", (e) => {
        const videoFile = document.getElementById('videoFile')
        videoFile.type = 'file';
        // Add the accept attribute 
        videoFile.attributes('accept', 'video/*');
      });

      // Add remove event to the button
      newObjective.querySelector(".option6").addEventListener("click", () => {
        const videoFile = document.getElementById('videoFile')
        videoFile.type = 'text';
        // Remove the accept attribute 
        videoFile.removeAttribute('accept');
      });

      // Add remove event to the button
        

      //newObjective.querySelector(".btn-save").addEventListener("click", () => {
       //alert(22)
      //});
      //const form = newObjective.querySelector(".courseForm");
      const form = document.querySelector(".courseForm");
      form.addEventListener("submit", (e) => {
        e.preventDefault();

        alert(122)
        if (!form.checkValidity()) {
          
          e.stopPropagation();
        }
        // Show Loading Spinner
        loadingSpinner.style.display = "flex";
        saveObject(form, csrfToken, loadingSpinner)
      });

      // Remove all child elements
      while (contentContainer.firstChild) {
        contentContainer.removeChild(contentContainer.firstChild)
      }

      contentContainer.appendChild(newObjective);

      