import { Descriptions } from "antd";

export default function SelectionResult({ selection }) {
  return <Descriptions bordered layout="horizontal" items={selection} />;
}
