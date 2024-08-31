import polars as pl
import os
import datetime
import pickle
import mlflow
from mlflow.tracking import MlflowClient
#Evidently
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric, ColumnQuantileMetric, ColumnCorrelationsMetric
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.ui.workspace import RemoteWorkspace, Workspace
from evidently.ui.dashboards import DashboardPanelCounter, DashboardPanelPlot, CounterAgg, PanelValue, PlotType, ReportFilter
from evidently.renderers.html_widgets import WidgetSize

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


EVIDENTLY_HOST = os.environ.get('EVIDENTLY_HOST', 'http://localhost:8000')
TRACKING_URI = os.environ.get("TRACKING_URI", "http://localhost:5000")
EXPERIMENT_NAME = os.environ.get("EXPERIMENT_NAME")

@data_exporter
def export_data(data, *args, **kwargs):
    logged_model, artifact_uri, run_id = data
    print(logged_model, artifact_uri, run_id)
    target = pl.col("Energy consumption")
    num_features = (
        '%Red Pixel',
        '%Green pixel',
        '%Blue pixel',
        'Hb'
    )

    # Load Model from MLFlow
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    # Load Data
    client = MlflowClient()
    tmp_path = client.download_artifacts(run_id, "models/train_df.pkl")
    with open(tmp_path, 'rb') as f:
        train_df = pickle.load(f)
    X_train = train_df.drop('target')
    Y_train = train_df['target'] 
    print("X_train, Y_train:", X_train, Y_train)

    tmp_path = client.download_artifacts(run_id, "models/test_df.pkl")
    with open(tmp_path, 'rb') as f:
        test_df = pickle.load(f)
    X_test = test_df.drop('target')
    Y_test = test_df['target'] 
    print("X_test, Y_test:", X_test, Y_test)
    # Evaluate

    pred = loaded_model.predict(X_train.to_pandas())
    df_train = X_train.with_columns(
        kwhTotal=pl.lit(Y_train.get_column('kwhTotal').to_list()),
        Pred_kwhTotal=pl.lit(pred)
    )
    pred = loaded_model.predict(X_test.to_pandas())
    df_test = X_test.with_columns(
        kwhTotal=pl.lit(Y_test.get_column('kwhTotal').to_list()),
        Pred_kwhTotal=pl.lit(pred)
    )
    # print(df_train)
    # Evidently Mapping
    column_mapping = ColumnMapping(
        target='kwhTotal',
        prediction='Pred_kwhTotal',
        numerical_features=num_features
    )
    
    # Evidently Report
    report = Report(
        metrics=[
            DatasetDriftMetric(),
            ColumnDriftMetric(column_name='%Red Pixel'),
            ColumnDriftMetric(column_name='%Green pixel'),
            ColumnDriftMetric(column_name='%Blue pixel'),
            ColumnDriftMetric(column_name='Hb'),
            ColumnDriftMetric(column_name='Pred_kwhTotal'),
            DatasetMissingValuesMetric()
        ],
        timestamp=datetime.datetime.now()
    )
    
    # create a workspace
    ws = RemoteWorkspace(EVIDENTLY_HOST)
    # print(ws)
    # print(df_train.to_pandas())

    # Reporting
    project = None
    projects = ws.search_project("Energy Consumption Prediction Project")
    print(projects)
    if len(projects) > 0:
        project = projects[0]
    else:
        project = ws.create_project("Energy Consumption Prediction Project")
        project.description = "Energy Consumption monitoring"
        project.save()
    
    report.run(reference_data=df_train.to_pandas(),
                    current_data=df_test.to_pandas(),
                    column_mapping=column_mapping)

    ws.add_report(project.id, report)

    # configure the dashboard
    project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Energy Consumption dashboard"
        )
    )

    project.dashboard.add_panel(
        DashboardPanelPlot(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            title="Inference Count",
            values=[
                PanelValue(
                    metric_id="DatasetSummaryMetric",
                    field_path="current.number_of_rows",
                    legend="count"
                ),
            ],
            plot_type=PlotType.BAR,
            size=WidgetSize.HALF,
        ),
    )

    project.dashboard.add_panel(
        DashboardPanelPlot(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            title="Number of Missing Values",
            values=[
                PanelValue(
                    metric_id="DatasetSummaryMetric",
                    field_path="current.number_of_missing_values",
                    legend="count"
                ),
            ],
            plot_type=PlotType.LINE,
            size=WidgetSize.HALF,
        ),
    )

    project.save()

