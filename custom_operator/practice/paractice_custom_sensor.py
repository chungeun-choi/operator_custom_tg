from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from practice.pracitce_custom_hook import MovielensHook

class MovielenRatinsSensor(BaseSensorOperator):
    template_fields = ("_start_date","end_date")

    @apply_defaults
    def __init__(self, conn_id, start_date="{{ds}}",end_date="{{next_ds}}",**kwargs):
        super().__init__(**kwargs)
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date
    

    def poke(self, context):
        hook = MovielensHook(self._conn_id)

        try:
            next(
                hook.get_ratings(
                    start_date= self._start_date,
                    end_date=self._end_date,
                    batch_size=1
                )
            )
            return True
        except StopIteration:
            self.log.info(
                f""
            )
            return False
        
        finally:
            hook.close()