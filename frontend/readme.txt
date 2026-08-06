COVEREDCALLDASHBOARD/
backend/
    backend/
        asgi.py
        settings.py
        urls.py
        wsgi.py

    portfolio/
        admin.py
        apps.py
        models.py
        serializers.py
        tests.py
        urls.py
        views.py
        
    create_superuser.py
    manage.py
    db.sqlite3
    Procfile
    requirements.txt
    runtime.txt

frontend/
    api.py
    config.py
    Dashboard.py
    services.py
    utils.py
    requirements.txt

    components/
        login.py
        sidebar.py
        kpi_cards.py
        charts.py
        tables.py
        navigation.py
        styles.py

        cash/
            add_form.py
            allocation_chart.py
            export_buttons.py
            holding_cards.py
            summary.py

        covered_calls/
            add_form.py
            close_position.py
            closed_card.py
            delete_position.py
            edit_position.py
            filters.py
            open_card.py
            summary.py

    pages/
        Cash_Holdings.py
        Covered_Calls.py

.gitignore