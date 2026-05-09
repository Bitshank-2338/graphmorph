import Header from "./Header";

export default function WorkspaceLayout({ left, center, right, connected }) {
  return (
    <div className="h-screen flex flex-col">
      <Header connected={connected} />
      <div className="flex-1 grid grid-cols-12 overflow-hidden">
        <div className="col-span-3 xl:col-span-2 overflow-hidden">{left}</div>
        <div className="col-span-6 xl:col-span-8 overflow-y-auto p-5">
          {center}
        </div>
        <div className="col-span-3 xl:col-span-2 overflow-hidden">{right}</div>
      </div>
    </div>
  );
}
