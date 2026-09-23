import React, { useState } from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';
import '../../styles/tokens.css';
import './DataTable.css';

export interface ColumnDef<T> {
  key: string;
  header: string;
  render?: (row: T) => React.ReactNode;
  sortable?: boolean;
}

export interface DataTableProps<T extends { id: string | number }> {
  columns: ColumnDef<T>[];
  data: T[];
  selectable?: boolean;
  onSelectionChange?: (selectedIds: (string | number)[]) => void;
  className?: string;
}

export function DataTable<T extends { id: string | number }>({
  columns,
  data,
  selectable = false,
  onSelectionChange,
  className = ''
}: DataTableProps<T>) {
  const [selectedIds, setSelectedIds] = useState<Set<string | number>>(new Set());
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  const toggleSelectAll = () => {
    if (selectedIds.size === data.length) {
      setSelectedIds(new Set());
      onSelectionChange?.([]);
    } else {
      const all = new Set(data.map((d) => d.id));
      setSelectedIds(all);
      onSelectionChange?.(Array.from(all));
    }
  };

  const toggleSelectRow = (id: string | number) => {
    const updated = new Set(selectedIds);
    if (updated.has(id)) {
      updated.delete(id);
    } else {
      updated.add(id);
    }
    setSelectedIds(updated);
    onSelectionChange?.(Array.from(updated));
  };

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  };

  const sortedData = [...data].sort((a: any, b: any) => {
    if (!sortKey) return 0;
    const valA = a[sortKey];
    const valB = b[sortKey];
    if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
    if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  return (
    <div className={`tech-datatable-wrapper ${className}`}>
      <table className="tech-datatable">
        <thead>
          <tr>
            {selectable && (
              <th className="tech-datatable__th tech-datatable__th--check">
                <input
                  type="checkbox"
                  checked={data.length > 0 && selectedIds.size === data.length}
                  onChange={toggleSelectAll}
                />
              </th>
            )}
            {columns.map((col) => (
              <th
                key={col.key}
                className={`tech-datatable__th ${col.sortable !== false ? 'tech-datatable__th--sortable' : ''}`}
                onClick={() => col.sortable !== false && handleSort(col.key)}
              >
                <div className="tech-datatable__th-content">
                  <span>{col.header}</span>
                  {sortKey === col.key && (
                    sortOrder === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row) => {
            const isSelected = selectedIds.has(row.id);
            return (
              <tr
                key={row.id}
                className={`tech-datatable__tr ${isSelected ? 'tech-datatable__tr--selected' : ''}`}
              >
                {selectable && (
                  <td className="tech-datatable__td tech-datatable__td--check">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => toggleSelectRow(row.id)}
                    />
                  </td>
                )}
                {columns.map((col) => (
                  <td key={col.key} className="tech-datatable__td">
                    {col.render ? col.render(row) : (row as any)[col.key]}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
