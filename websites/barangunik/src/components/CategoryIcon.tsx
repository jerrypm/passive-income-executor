import { Coins, Tag, Star, Gem, Crown, type LucideIcon } from "lucide-react";
import type { CategoryConfig } from "@/lib/constants";

const ICON_MAP: Record<CategoryConfig["iconName"], LucideIcon> = {
  coins: Coins,
  tag: Tag,
  star: Star,
  gem: Gem,
  crown: Crown,
};

interface CategoryIconProps {
  category: CategoryConfig;
  size?: "sm" | "md" | "lg";
}

const SIZES = {
  sm: { wrapper: "p-2", icon: "w-5 h-5" },
  md: { wrapper: "p-3", icon: "w-8 h-8" },
  lg: { wrapper: "p-4", icon: "w-10 h-10" },
};

export default function CategoryIcon({ category, size = "md" }: CategoryIconProps) {
  const Icon = ICON_MAP[category.iconName];
  const s = SIZES[size];

  return (
    <div className={`rounded-full ${category.iconBg} ${s.wrapper} inline-flex`}>
      <Icon className={`${s.icon} ${category.iconColor}`} />
    </div>
  );
}
