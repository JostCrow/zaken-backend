for filename in BPMN/*.bpmn; do
        bpmnlint "$filename"
    done
done
