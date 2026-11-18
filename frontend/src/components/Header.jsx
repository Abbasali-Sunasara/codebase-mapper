import { Workflow } from 'lucide-react';

export default function Header() {
  return <header className="page-header flex items-start justify-between"><div><p className="eyebrow"><Workflow size={14} /> CODEBASE EXPLORER</p><h1>Codebase Mapper</h1><p>Explore repository structure, dependencies, and code insights.</p></div></header>;
}
