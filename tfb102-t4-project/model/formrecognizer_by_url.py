#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# by url
def formrecognizer_by_url(formUrl):
    import os
    from azure.core.exceptions import ResourceNotFoundError
    from azure.ai.formrecognizer import FormRecognizerClient
    from azure.ai.formrecognizer import FormTrainingClient
    from azure.core.credentials import AzureKeyCredential

    # Set user key, endpoint
    key = "653310d794cd4bcba674b91918a7dc72"
    endpoint = "https://tfb102-t4-project.cognitiveservices.azure.com/"

    # call API
    form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
    trained_model_id = "73bebc87-1c6d-44da-84a1-ef7ed9a6a4a1"


    # URL
#     formUrl = "https://s.zimedia.com.tw/s/G5YEQz-3"

    poller = form_recognizer_client.begin_recognize_custom_forms_from_url(
        model_id=trained_model_id, form_url=formUrl)
    result = poller.result()

    output = {}

    for recognized_form in result:
        print("Form type: {}".format(recognized_form.form_type))
    #     print(recognized_form.fields)
        for name, field in recognized_form.fields.items():
            if name not in output:
                output[name]= str(field.value)
            else:
                output[name].append(field.value)

    output["年份"] = output["年份"][0:3]
    output["月份"] = output["月份"].split('-')[0].zfill(2)
    output["發票號碼"] = output["發票號碼"][-8:]
    output["日期"] = output["年份"][0:3]+output["月份"].split('-')[0].zfill(2)
    return output

if __name__ == '__main()__':
    formrecognizer_by_url(formUrl)

