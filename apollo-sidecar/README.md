# Apollo Notifier

## this tool will detect mysql which is used by Apollo periodically.
 * send notification to the matched webhook that defined in conf/config.yaml
 * metrics will be on the port 10010, it will shows like this:
 ```
 # HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 930.0
python_gc_objects_collected_total{generation="1"} 260.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 196.0
python_gc_collections_total{generation="1"} 17.0
python_gc_collections_total{generation="2"} 1.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="7",patchlevel="4",version="3.7.4"} 1.0
# HELP apollo_listener_sendwehook_s_total succeed
# TYPE apollo_listener_sendwehook_s_total counter
apollo_listener_sendwehook_s_total{appid="NON1001",cluster="default",namespace="application"} 1.0
# HELP apollo_listener_sendwehook_s_created succeed
# TYPE apollo_listener_sendwehook_s_created gauge
apollo_listener_sendwehook_s_created{appid="NON1001",cluster="default",namespace="application"} 1.6137410028617537e+09
# HELP apollo_listener_sendwehook_f_total failed
# TYPE apollo_listener_sendwehook_f_total counter
# HELP apollo_listener_sendwehook_o_total other
# TYPE apollo_listener_sendwehook_o_total counter
apollo_listener_sendwehook_o_total{appid="NON1001",cluster="default",namespace="NONconfiguration_items"} 1.0
apollo_listener_sendwehook_o_total{appid="NON1001",cluster="default",namespace="application"} 1.0
# HELP apollo_listener_sendwehook_o_created other
# TYPE apollo_listener_sendwehook_o_created gauge
apollo_listener_sendwehook_o_created{appid="NON1001",cluster="default",namespace="NONconfiguration_items"} 1.6137409727475553e+09
apollo_listener_sendwehook_o_created{appid="NON1001",cluster="default",namespace="application"} 1.613741002862258e+09

 ```