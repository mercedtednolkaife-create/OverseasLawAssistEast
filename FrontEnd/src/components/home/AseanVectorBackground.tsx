import React, { useId } from 'react';

interface AseanVectorBackgroundProps {
  className?: string;
  variant?: 'full' | 'compact';
}

/**
 * 仿 aiclipmaxx 现代极简矢量风格的东盟山海与日光射线背景
 *
 * 支持双模式：
 * 1. full: 主页全景版 (高 560~620px，包含完整天幕、34 束日光射线、远山、中景峰林、水面及左右海岬)
 * 2. compact: 非主页顶部极简精炼版 (高 180~220px，精巧晨曦、24 束细致射线与简明山脊线，底部迅速渐隐融入工作台底色)
 */
export const AseanVectorBackground: React.FC<AseanVectorBackgroundProps> = ({
  className = '',
  variant = 'full',
}) => {
  const uid = useId().replace(/:/g, '');

  const skyGradId = `skyGrad_${uid}`;
  const sunGlowId = `sunGlow_${uid}`;
  const sunRayGradId = `sunRayGrad_${uid}`;
  const farMtnGradId = `farMtnGrad_${uid}`;
  const midMtnGradId = `midMtnGrad_${uid}`;
  const waterGradId = `waterGrad_${uid}`;
  const nearMtnGradId = `nearMtnGrad_${uid}`;

  // ==========================================
  // 1. COMPACT 模式：用于非主页其它页面顶部
  // ==========================================
  if (variant === 'compact') {
    const cx = 720;
    const cy = 100;
    const rayCount = 24;
    const startAngle = -75.0;
    const endAngle = 75.0;
    const step = (endAngle - startAngle) / (rayCount - 1);

    const compactRays = Array.from({ length: rayCount }).map((_, i) => {
      const angDeg = startAngle + i * step;
      const angRad = (angDeg * Math.PI) / 180;
      const x1 = cx + 38 * Math.sin(angRad);
      const y1 = cy - 38 * Math.cos(angRad);
      const x2 = cx + 380 * Math.sin(angRad);
      const y2 = cy - 380 * Math.cos(angRad);
      const isDashed = i % 2 === 1;
      return {
        key: `c-ray-${i}`,
        x1: Number(x1.toFixed(1)),
        y1: Number(y1.toFixed(1)),
        x2: Number(x2.toFixed(1)),
        y2: Number(y2.toFixed(1)),
        strokeDash: isDashed ? '3 4' : undefined,
        strokeWidth: i % 3 === 0 ? 1 : 0.75,
        opacity: i % 2 === 0 ? 0.35 : 0.18,
      };
    });

    return (
      <div
        aria-hidden="true"
        className={`absolute top-0 left-0 right-0 h-[180px] sm:h-[220px] overflow-hidden pointer-events-none select-none z-0 ${className}`}
      >
        <svg
          viewBox="0 0 1440 240"
          preserveAspectRatio="xMidYMid slice"
          className="absolute top-0 left-0 w-full h-full"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id={skyGradId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#D8E8FD" />
              <stop offset="45%" stopColor="#EBF3FD" />
              <stop offset="85%" stopColor="#F6F8FA" />
            </linearGradient>

            <radialGradient id={sunGlowId} cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.95" />
              <stop offset="30%" stopColor="#FEF3C7" stopOpacity="0.75" />
              <stop offset="65%" stopColor="#BAE6FD" stopOpacity="0.35" />
              <stop offset="100%" stopColor="#3B82F6" stopOpacity="0" />
            </radialGradient>

            <linearGradient id={sunRayGradId} x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#2563EB" stopOpacity="0.45" />
              <stop offset="40%" stopColor="#38BDF8" stopOpacity="0.25" />
              <stop offset="85%" stopColor="#93C5FD" stopOpacity="0.06" />
              <stop offset="100%" stopColor="#BFDBFE" stopOpacity="0" />
            </linearGradient>

            <linearGradient id={farMtnGradId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#A5C4F0" stopOpacity="0.75" />
              <stop offset="100%" stopColor="#C8DCF5" stopOpacity="0.4" />
            </linearGradient>

            <linearGradient id={midMtnGradId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#5B7EBA" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#87A7D8" stopOpacity="0.55" />
            </linearGradient>

            <linearGradient id={waterGradId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#7E9ECE" />
              <stop offset="100%" stopColor="#B8CEEE" />
            </linearGradient>
          </defs>

          {/* 天空 */}
          <rect width="1440" height="240" fill={`url(#${skyGradId})`} />

          {/* 旭日光晕与细致射线 */}
          <circle cx={cx} cy={cy} r={120} fill={`url(#${sunGlowId})`} />
          <g>
            {compactRays.map((ray) => (
              <line
                key={ray.key}
                x1={ray.x1}
                y1={ray.y1}
                x2={ray.x2}
                y2={ray.y2}
                stroke={`url(#${sunRayGradId})`}
                strokeWidth={ray.strokeWidth}
                opacity={ray.opacity}
                strokeDasharray={ray.strokeDash}
              />
            ))}
          </g>

          {/* 太阳核心圆盘与微弱光轮 */}
          <circle cx={cx} cy={cy} r={28} fill="#FFFFFF" opacity="0.95" />
          <circle cx={cx} cy={cy} r={28} fill="none" stroke="#FDE68A" strokeWidth="1.5" opacity="0.75" />
          <circle cx={cx} cy={cy} r={46} fill="none" stroke="#93C5FD" strokeWidth="0.75" strokeDasharray="3 3" opacity="0.45" />

          {/* 远景山脊 */}
          <path
            d="M0 135 L120 115 L240 128 L380 98 L500 124 L620 108 L720 125 L840 104 L960 122 L1100 95 L1220 120 L1340 106 L1440 122 L1440 240 L0 240 Z"
            fill={`url(#${farMtnGradId})`}
          />
          <path
            d="M0 135 L120 115 L240 128 L380 98 L500 124 L620 108 L720 125 L840 104 L960 122 L1100 95 L1220 120 L1340 106 L1440 122"
            stroke="#FFFFFF"
            strokeWidth="0.75"
            opacity="0.45"
            fill="none"
          />

          {/* 中景简明峰峦 */}
          <path
            d="M0 152 L90 136 L190 148 L310 130 L430 150 L560 134 L680 152 L800 132 L920 150 L1050 132 L1180 152 L1310 134 L1440 146 L1440 240 L0 240 Z"
            fill={`url(#${midMtnGradId})`}
          />
          <path
            d="M0 152 L90 136 L190 148 L310 130 L430 150 L560 134 L680 152 L800 132 L920 150 L1050 132 L1180 152 L1310 134 L1440 146"
            stroke="#93C5FD"
            strokeWidth="1"
            opacity="0.6"
            fill="none"
          />

          {/* 水面与晨光倒影 */}
          <rect y="165" width="1440" height="75" fill={`url(#${waterGradId})`} opacity="0.75" />
          <ellipse cx={cx} cy="178" rx="90" ry="4" fill="#FFFFFF" opacity="0.55" />
          <ellipse cx={cx} cy="192" rx="55" ry="3" fill="#FFFFFF" opacity="0.38" />

          {/* 水波微纹 */}
          <path d="M 0 172 C 360 168, 720 176, 1080 170 L 1440 174" stroke="#FFFFFF" strokeWidth="0.5" opacity="0.3" fill="none" />
          <path d="M 0 188 C 280 184, 840 192, 1440 186" stroke="#BFDBFE" strokeWidth="0.5" opacity="0.25" fill="none" />
        </svg>

        {/* 底部平滑渐隐过度层：融入 #F6F8FA 底色 */}
        <div className="absolute inset-x-0 bottom-0 h-28 bg-gradient-to-b from-transparent via-[#F6F8FA]/60 to-[#F6F8FA]" />
      </div>
    );
  }

  // ==========================================
  // 2. FULL 模式：主页全幅深景版
  // ==========================================
  const cx = 720;
  const cy = 250;
  const rayCount = 34;
  const startAngle = -80.0;
  const endAngle = 80.0;
  const angleStep = (endAngle - startAngle) / (rayCount - 1);

  const rays = Array.from({ length: rayCount }).map((_, i) => {
    const angDeg = startAngle + i * angleStep;
    const angRad = (angDeg * Math.PI) / 180;
    const x1 = cx + 52 * Math.sin(angRad);
    const y1 = cy - 52 * Math.cos(angRad);
    const x2 = cx + 590 * Math.sin(angRad);
    const y2 = cy - 590 * Math.cos(angRad);
    const isDashed = i % 2 === 1;
    const isMajor = i % 4 === 0;

    return {
      key: `ray-${i}`,
      x1: Number(x1.toFixed(1)),
      y1: Number(y1.toFixed(1)),
      x2: Number(x2.toFixed(1)),
      y2: Number(y2.toFixed(1)),
      strokeDash: isDashed ? '4 5' : undefined,
      strokeWidth: isMajor ? 1.25 : 0.75,
      opacity: isMajor ? 0.42 : isDashed ? 0.22 : 0.32,
    };
  });

  return (
    <div
      aria-hidden="true"
      className={`absolute top-0 left-0 right-0 h-[560px] sm:h-[620px] overflow-hidden pointer-events-none select-none z-0 ${className}`}
    >
      <svg
        viewBox="0 0 1440 600"
        preserveAspectRatio="xMidYMid slice"
        className="absolute top-0 left-0 w-full h-full"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          {/* 1. 天空渐变 */}
          <linearGradient id={skyGradId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#CDE0FB" />
            <stop offset="38%" stopColor="#E2EDFC" />
            <stop offset="72%" stopColor="#EFF6FF" />
            <stop offset="100%" stopColor="#F6F8FA" />
          </linearGradient>

          {/* 2. 旭日光晕 */}
          <radialGradient id={sunGlowId} cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.95" />
            <stop offset="25%" stopColor="#FEF3C7" stopOpacity="0.85" />
            <stop offset="55%" stopColor="#BAE6FD" stopOpacity="0.45" />
            <stop offset="100%" stopColor="#3B82F6" stopOpacity="0" />
          </radialGradient>

          {/* 3. 矢量射线线性渐变 */}
          <linearGradient id={sunRayGradId} x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#2563EB" stopOpacity="0.55" />
            <stop offset="35%" stopColor="#38BDF8" stopOpacity="0.32" />
            <stop offset="75%" stopColor="#93C5FD" stopOpacity="0.1" />
            <stop offset="100%" stopColor="#BFDBFE" stopOpacity="0" />
          </linearGradient>

          {/* 4. 远景群山渐变 */}
          <linearGradient id={farMtnGradId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#93B4E5" stopOpacity="0.85" />
            <stop offset="100%" stopColor="#B8CEEE" stopOpacity="0.6" />
          </linearGradient>

          {/* 5. 中景山峰渐变 */}
          <linearGradient id={midMtnGradId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#4B6FA8" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#7294C8" stopOpacity="0.75" />
          </linearGradient>

          {/* 6. 海域海面渐变 */}
          <linearGradient id={waterGradId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#6B93CB" />
            <stop offset="55%" stopColor="#8BB0E2" />
            <stop offset="100%" stopColor="#B4CDF0" />
          </linearGradient>

          {/* 7. 近景海岬海岛渐变 */}
          <linearGradient id={nearMtnGradId} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#2C4875" stopOpacity="0.88" />
            <stop offset="100%" stopColor="#3D5F96" stopOpacity="0.72" />
          </linearGradient>
        </defs>

        {/* 1. 天空天幕背景 */}
        <rect width="1440" height="600" fill={`url(#${skyGradId})`} />

        {/* 2. 旭日光晕与辐射线束 */}
        <circle cx={cx} cy={cy} r={180} fill={`url(#${sunGlowId})`} />
        <g>
          {rays.map((ray) => (
            <line
              key={ray.key}
              x1={ray.x1}
              y1={ray.y1}
              x2={ray.x2}
              y2={ray.y2}
              stroke={`url(#${sunRayGradId})`}
              strokeWidth={ray.strokeWidth}
              opacity={ray.opacity}
              strokeDasharray={ray.strokeDash}
            />
          ))}
        </g>

        {/* 3. 太阳核心圆盘与光晕圆环 */}
        <circle cx={cx} cy={cy} r={40} fill="#FFFFFF" opacity={0.95} />
        <circle cx={cx} cy={cy} r={40} fill="none" stroke="#FDE68A" strokeWidth={2} opacity={0.8} />
        <circle cx={cx} cy={cy} r={62} fill="none" stroke="#93C5FD" strokeWidth={1} strokeDasharray="4 4" opacity={0.5} />
        <circle cx={cx} cy={cy} r={94} fill="none" stroke="#60A5FA" strokeWidth={0.75} strokeDasharray="6 6" opacity={0.35} />

        {/* 4. 远山实体色块与高光山脊线 */}
        <path
          d="M0 310 L110 270 L210 288 L340 236 L460 282 L550 260 L680 292 L780 252 L880 284 L1000 242 L1120 285 L1240 256 L1350 288 L1440 272 L1440 370 L0 370 Z"
          fill={`url(#${farMtnGradId})`}
        />
        <path
          d="M0 310 L110 270 L210 288 L340 236 L460 282 L550 260 L680 292 L780 252 L880 284 L1000 242 L1120 285 L1240 256 L1350 288 L1440 272"
          stroke="#FFFFFF"
          strokeWidth={1}
          opacity={0.45}
          fill="none"
        />

        {/* 5. 中景山峰实体色块与山脊轮廓线 */}
        <path
          d="M0 338 L80 310 L180 326 L260 294 L370 332 L470 306 L570 336 L670 302 L760 330 L870 298 L980 334 L1080 306 L1190 338 L1300 308 L1390 328 L1440 320 L1440 400 L0 400 Z"
          fill={`url(#${midMtnGradId})`}
        />
        <path
          d="M0 338 L80 310 L180 326 L260 294 L370 332 L470 306 L570 336 L670 302 L760 330 L870 298 L980 334 L1080 306 L1190 338 L1300 308 L1390 328 L1440 320"
          stroke="#93C5FD"
          strokeWidth={1.25}
          opacity={0.65}
          fill="none"
        />

        {/* 6. 海洋水面色块 */}
        <rect y="372" width="1440" height="228" fill={`url(#${waterGradId})`} opacity={0.88} />

        {/* 7. 水面日照倒影光斑 */}
        <ellipse cx={cx} cy="392" rx="140" ry="6" fill="#FFFFFF" opacity={0.65} />
        <ellipse cx={cx} cy="412" rx="100" ry="4.5" fill="#FFFFFF" opacity="0.5" />
        <ellipse cx={cx} cy="432" rx="70" ry="3.5" fill="#FFFFFF" opacity="0.38" />
        <ellipse cx={cx} cy="452" rx="45" ry="2.5" fill="#FFFFFF" opacity="0.25" />

        {/* 8. 海流与波纹矢量线 */}
        <path
          d="M 0 382 C 240 375, 480 389, 720 382 C 960 375, 1200 389, 1440 382"
          stroke="#FFFFFF"
          strokeWidth={0.75}
          opacity={0.4}
          fill="none"
        />
        <path
          d="M 0 405 C 220 397, 460 413, 700 405 C 940 397, 1180 413, 1440 405"
          stroke="#FFFFFF"
          strokeWidth={0.75}
          opacity={0.3}
          fill="none"
        />
        <path
          d="M 0 432 C 260 423, 520 439, 760 432 C 1000 423, 1240 439, 1440 432"
          stroke="#BFDBFE"
          strokeWidth={0.75}
          opacity={0.25}
          fill="none"
        />
        <path
          d="M 0 465 C 240 455, 500 473, 740 465 C 980 455, 1220 473, 1440 465"
          stroke="#BFDBFE"
          strokeWidth={0.5}
          opacity={0.2}
          fill="none"
        />

        {/* 9. 近景左右海角岬湾 */}
        <path
          d="M0 480 C110 450 210 465 310 445 C400 425 470 455 550 490 C610 520 650 555 700 600 L0 600 Z"
          fill={`url(#${nearMtnGradId})`}
        />
        <path
          d="M0 480 C110 450 210 465 310 445 C400 425 470 455 550 490 C610 520 650 555 700 600"
          stroke="#60A5FA"
          strokeWidth={1.25}
          opacity={0.5}
          fill="none"
        />

        <path
          d="M1440 490 C1340 460 1250 475 1160 455 C1070 435 1010 465 940 500 C890 525 850 560 810 600 L1440 600 Z"
          fill={`url(#${nearMtnGradId})`}
          opacity={0.92}
        />
        <path
          d="M1440 490 C1340 460 1250 475 1160 455 C1070 435 1010 465 940 500 C890 525 850 560 810 600"
          stroke="#60A5FA"
          strokeWidth={1.25}
          opacity={0.5}
          fill="none"
        />
      </svg>

      {/* 底部平滑渐隐过渡层 */}
      <div className="absolute inset-x-0 bottom-0 h-44 sm:h-56 bg-gradient-to-b from-transparent via-[#F6F8FA]/50 to-[#F6F8FA]" />
    </div>
  );
};
