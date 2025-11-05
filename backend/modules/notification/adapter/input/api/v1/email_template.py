from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Body, Depends
import minify_html

from modules.notification.adapter.input.api.v1.request import (CreateEmailTemplateRequest)
from modules.notification.application.service.email_template import (EmailTemplateService)
from modules.notification.container import NotificationContainer
from modules.notification.domain.command import EditEmailTemplateCommand
from modules.notification.domain.entity.email_template import (EmailTemplate)


email_templates_router = APIRouter()


@email_templates_router.get("")
@inject
async def get_all_email_templates(
	email_templates_service: EmailTemplateService = Depends(
		Provide[NotificationContainer.email_template_service]
	),
):
	email_templates = await email_templates_service.get_all_email_templates()
	return email_templates


@email_templates_router.get("/{email_template_id}")
@inject
async def get_email_template_by_id(
	email_template_id: int,
	email_templates_service: EmailTemplateService = Depends(
		Provide[NotificationContainer.email_template_service]
	),
):
	email_template = await email_templates_service.get_email_template_by_id(
		email_template_id
	)
	return email_template


@email_templates_router.get("/by_name/{email_template_name}")
@inject
async def get_email_template_by_name(
	email_template_name: str,
	email_templates_service: EmailTemplateService = Depends(
		Provide[NotificationContainer.email_template_service]
	),
):
	email_template = await email_templates_service.get_email_template_by_name(
		email_template_name
	)
	return email_template


@email_templates_router.get("/by_module/{email_template_module}")
@inject
async def get_email_template_by_module(
	email_template_module: str,
	email_templates_service: EmailTemplateService = Depends(
		Provide[NotificationContainer.email_template_service]
	),
):
	email_template = await email_templates_service.get_email_template_by_module(
		email_template_module
	)
	return email_template


@email_templates_router.post("")
@inject
async def save_email_template(
	name: str,
	description: str,
	module: str,
	template: str = Body(..., media_type="plain/text"),
	email_templates_service: EmailTemplateService = Depends(
		Provide[NotificationContainer.email_template_service]
	),
):
	minified = minify_html.minify(template, minify_css=True, minify_js=True, minify_doctype=True, remove_processing_instructions=True)
	command = EmailTemplate(
		id=None,
		name=name,
		description=description,
		module=module,
		template_html=minified.encode("utf-8"),
	)

	new_email_template = await email_templates_service.save_email_template(command)
	return new_email_template


@email_templates_router.put("/{email_template_id}")
@inject
async def edit_email_template(
	email_template_id: int,
	name: str | None = None,
	description: str | None = None,
	module: str | None = None,
	template: str | None = Body(None, media_type="plain/text"),
	email_templates_service: EmailTemplateService = Depends(
		Provide[NotificationContainer.email_template_service]
	),
):
	tmp_template = None
	if template:
		#TODO: trasladar el minify a la capa de servicio
		minified = minify_html.minify(template, minify_css=True, minify_js=True, minify_doctype=True, remove_processing_instructions=True)
		tmp_template = minified.encode("utf-8")
	command = EditEmailTemplateCommand(
		name=name,
		description=description,
		module=module,
		template_html=tmp_template,
	)

	edited_email_template = await email_templates_service.edit_email_template(
		email_template_id, command
	)
	return edited_email_template


@email_templates_router.delete("/{email_template_id}")
@inject
async def delete_email_template(
	email_template_id: int,
	email_templates_service: EmailTemplateService = Depends(
		Provide[NotificationContainer.email_template_service]
	),
):
	await email_templates_service.delete_email_template(email_template_id)
	return {"detail": "Email template deleted successfully"}


# @email_templates_router.post("/send")
# @inject
# async def send_email_template(
# 	template: str = Body(..., media_type="plain/text"),
# 	email_templates_service: EmailTemplateService = Depends(
# 		Provide[NotificationContainer.email_template_service]
# 	),
# ):
# 	await email_templates_service.send_email_template(
# 		receiver_email=["ivanche.alejo@gmail.com"],
# 		subject="Test Email",
# 		body=template
# 	)
