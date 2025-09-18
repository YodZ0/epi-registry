import { useState } from "react";

import Layout from "./Layout";
import ASMSelectionForm from "./components/ASMSelectionForm";
import SelectionResult from "./components/SelectionResult";

const initialItems = [
  {
    key: "tier_1",
    label: "Предпочтительные",
    children: "Пусто",
    span: "filled",
  },
  {
    key: "tier_2",
    label: "Альтернативные",
    children: "Пусто",
    span: "filled",
  },
  {
    key: "tier_3",
    label: "Менее предпочтительные",
    children: "Пусто",
    span: "filled",
  },
  {
    key: "tier_4",
    label: "Наименее желательные / противопоказанные",
    children: "Пусто",
    span: "filled",
  },
];

const mapTier = {
  tier_1: "Предпочтительные",
  tier_2: "Альтернативные",
  tier_3: "Менее предпочтительные",
  tier_4: "Наименее желательные / противопоказанные",
};

function tiersToItems(data) {
  return Object.entries(data.tiers).map(([key, list]) => ({
    key,
    label: mapTier[key],
    children: list.join(", "),
    span: "filled",
  }));
}

export default function App() {
  const [selection, setSelection] = useState(initialItems);

  const onSuccess = (data) => {
    console.log("Recieved data on APP level: ", data);
    const items = tiersToItems(data);
    setSelection(items);
  };

  return (
    <Layout>
      <div className="grid grid-cols-24 gap-8">
        <div className="col-span-12">
          <div className="flex flex-col justify-center">
            <div className="flex text-xl justify-center mb-4">
              Данные о пациенте
            </div>
            <ASMSelectionForm onSuccess={onSuccess} />
          </div>
        </div>
        <div className="col-span-12">
          <div className="flex flex-col justify-center">
            <div className="flex text-xl justify-center mb-4">
              Рекомендации АЭП по группам
            </div>
            <SelectionResult selection={selection} />
          </div>
        </div>
      </div>
    </Layout>
  );
}
