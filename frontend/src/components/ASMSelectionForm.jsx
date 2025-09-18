import {
  Button,
  Checkbox,
  Form,
  InputNumber,
  Select,
  Radio,
  Row,
  Col,
} from "antd";

import { useModifiers } from "../api/queries/useModifiers";
import { useSeizureTypes } from "../api/queries/useSeizureTypes";
import { useASMSelection } from "../api/mutations/useASMSelection";

export default function ASMSelectionForm({ onSuccess }) {
  const { data: seizureTypesOptions } = useSeizureTypes();
  const { data: modifiersOptions } = useModifiers();
  // console.log("[DEBUG] Recieved seizure types: ", seizureTypesOptions);
  // console.log("[DEBUG] Recieved modifiers: ", modifiersOptions);

  const onRadioChange = (value) => {
    console.log("[DEBUG] gender changed = ", value.target.value);
  };

  const onMultiselectChange = (selectedValues) => {
    console.log("[DEBUG] selected = ", selectedValues);
  };

  const onCheckBoxChange = (checkedValues) => {
    console.log("[DEBUG] checked = ", checkedValues);
  };

  const { mutate: getSelection } = useASMSelection({
    onSuccess: (data) => {
      console.log("[DEBUG] Recieved data in form (onSuccess):", data);
      onSuccess(data);
    },
  });

  const onFormFinish = (values) => {
    console.log("[DEBUG] Success form finish:", values);
    getSelection(values);
  };

  const onFormFinishFailed = (errorInfo) => {
    console.log("[DEBUG] Failed:", errorInfo);
  };

  return (
    <Form
      name="asmForm"
      size="small"
      layout="vertical"
      autoComplete="off"
      onFinish={onFormFinish}
      onFinishFailed={onFormFinishFailed}
    >
      <Form.Item label="Пол" name="gender" initialValue={"male"}>
        <Radio.Group
          onChange={onRadioChange}
          options={[
            { value: "male", label: "Мужчина" },
            { value: "female", label: "Женщина" },
          ]}
        />
      </Form.Item>

      <Form.Item
        label="Возраст"
        name="age"
        rules={[
          { required: true, message: "Пожалуйста, укажите возраст пациента!" },
        ]}
      >
        <InputNumber placeholder="Input age" style={{ width: "100%" }} />
      </Form.Item>

      <Form.Item
        label="Вес, кг"
        name="weight"
        rules={[
          { required: true, message: "Пожалуйста, введите вес пациента!" },
        ]}
      >
        <InputNumber
          step={0.1}
          placeholder="Input weight"
          style={{ width: "100%" }}
        />
      </Form.Item>

      <Form.Item
        label="Типы приступов"
        name="seizureTypes"
        rules={[
          { required: true, message: "Пожалуйста, выберите типы приступов!" },
        ]}
      >
        <Select
          mode="multiple"
          allowClear
          placeholder="Select seizure types"
          onChange={onMultiselectChange}
          options={seizureTypesOptions}
        />
      </Form.Item>

      <Form.Item
        label="Модификаторы:"
        name="modifiers"
        rules={[
          { required: true, message: "Пожалуйста, укажите модификаторы!" },
        ]}
      >
        <Checkbox.Group onChange={onCheckBoxChange}>
          <Row gutter={[4, 8]}>
            {modifiersOptions?.map((m) => (
              <Col span={12} key={m.value}>
                <Checkbox value={m.value}>{m.label}</Checkbox>
              </Col>
            ))}
          </Row>
        </Checkbox.Group>
      </Form.Item>

      <Form.Item label={null}>
        <div className="flex justify-center my-2">
          <Button type="primary" htmlType="submit" size="large">
            Отправить
          </Button>
        </div>
      </Form.Item>
    </Form>
  );
}
