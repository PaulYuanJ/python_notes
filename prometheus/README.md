# 在Vbox环境的kubernetes下安装了一套监控系统

## 通过命令找到prometheus的url
```
# kubectl get all -n monitoring
NAME                                       READY   STATUS    RESTARTS   AGE
pod/alertmanager-main-0                    2/2     Running   4          7d23h
pod/blackbox-exporter-8485dc4b9d-7df5d     3/3     Running   6          7d23h
pod/grafana-6b44fd78c-qvhlt                1/1     Running   2          7d23h
pod/kube-state-metrics-58b7f755dd-ndd45    3/3     Running   6          7d23h
pod/node-exporter-cgwm4                    2/2     Running   4          7d23h
pod/node-exporter-wm45x                    2/2     Running   4          7d23h
pod/prometheus-adapter-5d89d87dc-hjbrj     1/1     Running   2          7d23h
pod/prometheus-k8s-0                       2/2     Running   5          7d23h
pod/prometheus-operator-7649c7454f-k47s4   2/2     Running   4          7d23h

NAME                            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
service/alertmanager-main       NodePort    10.110.161.2     <none>        9093:30093/TCP               7d23h
service/alertmanager-operated   ClusterIP   None             <none>        9093/TCP,9094/TCP,9094/UDP   7d23h
service/blackbox-exporter       ClusterIP   10.107.82.189    <none>        9115/TCP,19115/TCP           7d23h
service/grafana                 NodePort    10.110.218.222   <none>        3000:30030/TCP               7d23h
service/kube-state-metrics      ClusterIP   None             <none>        8443/TCP,9443/TCP            7d23h
service/node-exporter           ClusterIP   None             <none>        9100/TCP                     7d23h
service/prometheus-adapter      ClusterIP   10.99.24.235     <none>        443/TCP                      7d23h
service/prometheus-k8s          NodePort    10.109.153.230   <none>        9090:30090/TCP               7d23h
service/prometheus-operated     ClusterIP   None             <none>        9090/TCP                     7d23h
service/prometheus-operator     ClusterIP   None             <none>        8443/TCP                     7d23h

NAME                           DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
daemonset.apps/node-exporter   2         2         2       2            2           kubernetes.io/os=linux   7d23h

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/blackbox-exporter     1/1     1            1           7d23h
deployment.apps/grafana               1/1     1            1           7d23h
deployment.apps/kube-state-metrics    1/1     1            1           7d23h
deployment.apps/prometheus-adapter    1/1     1            1           7d23h
deployment.apps/prometheus-operator   1/1     1            1           7d23h

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/blackbox-exporter-8485dc4b9d     1         1         1       7d23h
replicaset.apps/grafana-6b44fd78c                1         1         1       7d23h
replicaset.apps/grafana-6d869f6f9f               0         0         0       7d23h
replicaset.apps/grafana-6dbbd5566d               0         0         0       7d23h
replicaset.apps/grafana-c78d94484                0         0         0       7d23h
replicaset.apps/kube-state-metrics-58b7f755dd    1         1         1       7d23h
replicaset.apps/prometheus-adapter-5579d9df79    0         0         0       7d23h
replicaset.apps/prometheus-adapter-5d89d87dc     1         1         1       7d23h
replicaset.apps/prometheus-adapter-6f9cdc74dc    0         0         0       7d23h
replicaset.apps/prometheus-operator-7649c7454f   1         1         1       7d23h

NAME                                 READY   AGE
statefulset.apps/alertmanager-main   1/1     7d23h
statefulset.apps/prometheus-k8s      1/1     7d23h
```

## 封装HTTP API 
根据prometheus官方的HTTP API封装一个prometheus的client，详见PrometheusQueryClient.py