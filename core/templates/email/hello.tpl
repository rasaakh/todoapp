{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello Activation
{% endblock %}

{% block html %}

{{token}}
{% endblock %}