# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin: CJK Metrics
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from Foundation import NSAffineTransform, NSBezierPath, NSColor
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *


CJK_GUIDE_GLYPH = '_cjkguide'


class CJKMetrics(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'CJK Metrics',
			'zh': u'汉字度量',
			'ja': u'CJK メトリクス',
		})

		self.medialAxesState = True
		self.centralAreaState = True
		self.centralAreaRotateState = False
		self.cjkGuideState = True
		self.cjkGuideScalingState = False
		self.centralAreaDivisionState = 2  # New state for division (2 or 3)
		self.tripartiteDivisionState = False  # New state for tripartite division lines
		self.tripartiteDivisionBasis = 100.0  # Default to 100% of the virtual body

		self.centralAreaSpacing = 100.0  # Default to 100%
		self.centralAreaWidth = 100.0
		self.centralAreaPosition = 50.0

		self.windowCentralArea = Window((200, 60))
		self.windowCentralArea.group = Group((0, 0, 200, 60))
		self.windowCentralArea.group.textBoxSpacing = TextBox(
			Glyphs.localize({
				'en': (30, 4, 50, 16),
				'zh': (30, 4, 30, 16),
				'ja': (30, 4, 50, 16),
			}),
			text=Glyphs.localize({
				'en': u'Spacing',
				'zh': u'间距',
				'ja': u'間隔',
			}),
			sizeStyle='small',
		)
		self.windowCentralArea.group.editTextSpacing = EditText(
			Glyphs.localize({
				'en': (85, 2, 60, 16),
				'zh': (65, 2, 60, 16),
				'ja': (85, 2, 60, 16),
			}),
			sizeStyle='small',
			placeholder='100',
			callback=self.editTextCentralAreaSpacingCallback,
		)
		self.windowCentralArea.group.textBoxSpacingValue = TextBox(
			Glyphs.localize({
				'en': (150, 4, 50, 16),
				'zh': (130, 4, 50, 16),
				'ja': (150, 4, 50, 16),
			}),
			text='{}%'.format(self.centralAreaSpacing),
			sizeStyle='small',
		)
		self.windowCentralArea.group.textBoxWidth = TextBox(
			Glyphs.localize({
				'en': (30, 24, 50, 16),
				'zh': (30, 24, 30, 16),
				'ja': (30, 24, 50, 16),
			}),
			text=Glyphs.localize({
				'en': u'Width',
				'zh': u'宽度',
				'ja': u'幅',
			}),
			sizeStyle='small',
		)
		self.windowCentralArea.group.editTextWidth = EditText(
			Glyphs.localize({
				'en': (85, 22, 60, 16),
				'zh': (65, 22, 60, 16),
				'ja': (85, 22, 60, 16),
			}),
			sizeStyle='small',
			placeholder='100',
			callback=self.editTextCentralAreaWidthCallback,
		)
		self.windowCentralArea.group.textBoxPosition = TextBox(
			Glyphs.localize({
				'en': (30, 44, 50, 16),
				'zh': (30, 44, 30, 16),
				'ja': (30, 44, 50, 16),
			}),
			text=Glyphs.localize({
				'en': u'Position',
				'zh': u'位置',
				'ja': u'位置',
			}),
			sizeStyle='small',
		)
		self.windowCentralArea.group.editTextPosition = EditText(
			Glyphs.localize({
				'en': (85, 42, 60, 16),
				'zh': (65, 42, 60, 16),
				'ja': (85, 42, 60, 16),
			}),
			sizeStyle='small',
			placeholder='50',
			callback=self.editTextCentralAreaPositionCallback,
		)
		self.windowCentralArea.group.textBoxPositionValue = TextBox(
			Glyphs.localize({
				'en': (150, 44, 50, 16),
				'zh': (130, 44, 50, 16),
				'ja': (150, 44, 50, 16),
			}),
			text='{}%'.format(self.centralAreaPosition),
			sizeStyle='small',
		)

		self.windowTripartiteDivision = Window((200, 30))
		self.windowTripartiteDivision.group = Group((0, 0, 200, 30))
		self.windowTripartiteDivision.group.textBoxBasis = TextBox(
			Glyphs.localize({
				'en': (30, 4, 50, 16),
				'zh': (30, 4, 30, 16),
				'ja': (30, 4, 50, 16),
			}),
			text=Glyphs.localize({
				'en': u'Basis Size',
				'zh': u'基准字面大小',
				'ja': u'基準字面サイズ',
			}),
			sizeStyle='small',
		)
		self.windowTripartiteDivision.group.editTextBasis = EditText(
			Glyphs.localize({
				'en': (85, 2, 60, 16),
				'zh': (65, 2, 60, 16),
				'ja': (85, 2, 60, 16),
			}),
			sizeStyle='small',
			placeholder='100',
			callback=self.editTextTripartiteDivisionBasisCallback,
		)

		self.generalContextMenus = self.buildContextMenus()

	@objc.python_method
	def editTextCentralAreaSpacingCallback(self, sender):
		self.centralAreaSpacing = toFloat(sender.get())

	@objc.python_method
	def editTextCentralAreaWidthCallback(self, sender):
		self.centralAreaWidth = toFloat(sender.get())

	@objc.python_method
	def editTextCentralAreaPositionCallback(self, sender):
		self.centralAreaPosition = toFloat(sender.get())
		self.windowCentralArea.group.textBoxPositionValue.set('{:.1f}%'.format(self.centralAreaPosition))

	@objc.python_method
	def editTextTripartiteDivisionBasisCallback(self, sender):
		self.tripartiteDivisionBasis = toFloat(sender.get())

	@objc.python_method
	def buildContextMenus(self):
		return [
			{
				'name': Glyphs.localize({
					'en': u'CJK Metrics Options:',
					'zh': u'汉字度量选项：',
					'ja': u'CJK メトリクス オプション：',
				}),
				'action': None,
			},
			{
				'name': Glyphs.localize({
					'en': u'Show Medial Axes',
					'zh': u'显示水平垂直轴线',
					'ja': u'中心線を表示',
				}),
				'action': self.toggleMedialAxes,
				'state': self.medialAxesState,
			},
			{
				'name': Glyphs.localize({
					'en': u'Show Tripartite Division Lines',
					'zh': u'显示三等分线',
					'ja': u'三等分線を表示',
				}),
				'action': self.toggleTripartiteDivision,
				'state': self.tripartiteDivisionState,
			},
			{
				'view': self.windowTripartiteDivision.group.getNSView(),
			},
			{
				'name': Glyphs.localize({
					'en': u'Show Central Area',
					'zh': u'显示第二中心区域',
					'ja': u'中央エリアを表示',
				}),
				'action': self.toggleCentralArea,
				'state': self.centralAreaState,
			},
			{
				'name': Glyphs.localize({
					'en': u'Rotate Central Area',
					'zh': u'旋转第二中心区域',
					'ja': u'中央エリアを回転',
				}),
				'action': self.rotateCentralArea,
				'state': self.centralAreaRotateState,
			},
			{
				'name': Glyphs.localize({
					'en': u'Divide Central Area into Three',
					'zh': u'将中心区域分为三部分',
					'ja': u'中央エリアを3つに分割',
				}),
				'action': self.toggleCentralAreaDivision,
				'state': self.centralAreaDivisionState == 3,
			},
			{
				'view': self.windowCentralArea.group.getNSView(),
			},
			{
				'name': Glyphs.localize({
					'en': u'Show CJK Guide',
					'zh': u'显示汉字参考线',
					'ja': u'CJK ガイドを表示',
				}),
				'action': self.toggleCjkGuide,
				'state': self.cjkGuideState,
			},
			{
				'name': Glyphs.localize({
					'en': u'Scale CJK Guide',
					'zh': u'缩放汉字参考线',
					'ja': u'CJK ガイドをスケール',
				}),
				'action': self.toggleCjkGuideScaling,
				'state': self.cjkGuideScalingState,
			},
		]

	def toggleMedialAxes(self):
		self.medialAxesState = not self.medialAxesState
		self.generalContextMenus = self.buildContextMenus()

	def toggleCentralArea(self):
		self.centralAreaState = not self.centralAreaState
		if self.centralAreaState:
			self.windowCentralArea.group.textBoxSpacing.enable(True)
			self.windowCentralArea.group.editTextSpacing.enable(True)
			self.windowCentralArea.group.textBoxWidth.enable(True)
			self.windowCentralArea.group.editTextWidth.enable(True)
			self.windowCentralArea.group.textBoxPosition.enable(True)
			self.windowCentralArea.group.editTextPosition.enable(True)
			self.windowCentralArea.group.textBoxPositionValue.enable(True)
		else:
			self.windowCentralArea.group.textBoxSpacing.enable(False)
			self.windowCentralArea.group.editTextSpacing.enable(False)
			self.windowCentralArea.group.textBoxWidth.enable(False)
			self.windowCentralArea.group.editTextWidth.enable(False)
			self.windowCentralArea.group.textBoxPosition.enable(False)
			self.windowCentralArea.group.editTextPosition.enable(False)
			self.windowCentralArea.group.textBoxPositionValue.enable(False)
		self.generalContextMenus = self.buildContextMenus()

	def rotateCentralArea(self):
		self.centralAreaRotateState = not self.centralAreaRotateState
		self.generalContextMenus = self.buildContextMenus()

	def toggleCjkGuide(self):
		self.cjkGuideState = not self.cjkGuideState
		self.generalContextMenus = self.buildContextMenus()

	def toggleCjkGuideScaling(self):
		self.cjkGuideScalingState = not self.cjkGuideScalingState
		self.generalContextMenus = self.buildContextMenus()

	def toggleCentralAreaDivision(self):
		self.centralAreaDivisionState = 3 if self.centralAreaDivisionState == 2 else 2
		self.generalContextMenus = self.buildContextMenus()

	def toggleTripartiteDivision(self):
		self.tripartiteDivisionState = not self.tripartiteDivisionState
		self.generalContextMenus = self.buildContextMenus()

	@objc.python_method
	def foreground(self, layer):
		if self.medialAxesState:
			self.drawMedialAxes(layer)
		if self.centralAreaState:
			self.drawCentralArea(layer)
		if self.cjkGuideState:
			self.drawCjkGuide(layer)
		if self.tripartiteDivisionState:
			self.drawTripartiteDivisionLines(layer)

	@objc.python_method
	def drawMedialAxes(self, layer):
		'''Draw the medial axes (水平垂直轴线).'''
		# TODO: set vertical and horizontal in dialog
		vertical = 0.5
		horizontal = 0.5

		scale = self.getScale()

		view = Glyphs.font.currentTab.graphicView()
		visibleRect = view.visibleRect()
		activePosition = view.activePosition()

		viewOriginX = (visibleRect.origin.x - activePosition.x) / scale
		viewOriginY = (visibleRect.origin.y - activePosition.y) / scale
		viewWidth = visibleRect.size.width / scale
		viewHeight = visibleRect.size.height / scale

		height = layer.ascender - layer.descender
		width  = layer.width

		x = horizontal * width
		y = layer.descender + vertical * height

		# TODO: color
		color = NSColor.systemGreenColor()
		color.set()

		path = NSBezierPath.bezierPath()
		path.moveToPoint_((viewOriginX, y))
		path.lineToPoint_((viewOriginX + viewWidth, y))
		path.moveToPoint_((x, viewOriginY))
		path.lineToPoint_((x, viewOriginY + viewHeight))
		path.setLineWidth_(1 / scale)
		path.stroke()

	@objc.python_method
	def drawCentralArea(self, layer):
		'''Draw the central area (第二中心区域).'''
		descender = layer.descender
		ascender = layer.ascender

		if not self.centralAreaRotateState:
			# Calculate the actual spacing based on the width
			division_factor = 3 if self.centralAreaDivisionState == 3 else 2
			actual_spacing = (layer.width * self.centralAreaSpacing / 100) / division_factor

			width = self.centralAreaWidth
			height = ascender - descender
			x_mid = layer.width * self.centralAreaPosition / 100

			if self.centralAreaDivisionState == 3:
				# Adjust positions for three divisions to center the second area
				(x0, y0) = (x_mid - actual_spacing - width / 2, descender)
				(x1, y1) = (x_mid - width / 2, descender)
				(x2, y2) = (x_mid + actual_spacing - width / 2, descender)
				positions = [(x0, y0), (x1, y1), (x2, y2)]
			else:
				# Default to two divisions
				(x0, y0) = (x_mid - actual_spacing / 2 - width / 2, descender)
				(x1, y1) = (x_mid + actual_spacing / 2 - width / 2, descender)
				positions = [(x0, y0), (x1, y1)]
		else:
			# Calculate the actual spacing based on the height
			division_factor = 3 if self.centralAreaDivisionState == 3 else 2
			actual_spacing = ((ascender - descender) * self.centralAreaSpacing / 100) / division_factor

			width = layer.width
			height = self.centralAreaWidth
			y_mid = descender + (ascender - descender) * self.centralAreaPosition / 100

			if self.centralAreaDivisionState == 3:
				# Adjust positions for three divisions to center the second area
				(x0, y0) = (0, y_mid - actual_spacing - height / 2)
				(x1, y1) = (0, y_mid - height / 2)
				(x2, y2) = (0, y_mid + actual_spacing - height / 2)
				positions = [(x0, y0), (x1, y1), (x2, y2)]
			else:
				# Default to two divisions
				(x0, y0) = (0, y_mid - actual_spacing / 2 - height / 2)
				(x1, y1) = (0, y_mid + actual_spacing / 2 - height / 2)
				positions = [(x0, y0), (x1, y1)]

		# TODO: color
		color = NSColor.systemGrayColor().colorWithAlphaComponent_(0.2)
		color.set()

		for (x, y) in positions:
			NSBezierPath.fillRect_(((x, y), (width, height)))

	@objc.python_method
	def drawCjkGuide(self, layer):
		'''Draw the CJK guide (汉字参考线).'''
		self.initCjkGuideGlyph()

		# TODO: color
		color = NSColor.systemOrangeColor().colorWithAlphaComponent_(0.1)
		color.set()

		cjkGuideLayer = Glyphs.font.glyphs[CJK_GUIDE_GLYPH].layers[0]

		trans = NSAffineTransform.transform()
		if self.cjkGuideScalingState:
			# TODO: currently only xScale is necessary
			# cjkGuideMaster = cjkGuideLayer.associatedFontMaster()
			# cjkGuideDescender = cjkGuideMaster.descender
			# cjkGuideAscender = cjkGuideMaster.ascender
			# cjkGuideHeight = cjkGuideAscender - cjkGuideDescender

			# master = layer.associatedFontMaster()
			# descender = master.descender
			# ascender = master.ascender
			# height = ascender - descender

			xScale = layer.width / cjkGuideLayer.width
			# yScale = height / cjkGuideHeight

			# trans.translateXBy_yBy_(0, cjkGuideDescender)
			# trans.scaleXBy_yBy_(xScale, yScale)
			# trans.translateXBy_yBy_(0, -descender)

			trans.scaleXBy_yBy_(xScale, 1)

		if cjkGuideLayer.bezierPath is not None:
			path = cjkGuideLayer.bezierPath.copy()
			path.transformUsingAffineTransform_(trans)
			path.fill()

	@objc.python_method
	def initCjkGuideGlyph(self):
		font = Glyphs.font
		if font.glyphs[CJK_GUIDE_GLYPH] is None:
			# TODO: dialogue
			font.glyphs.append(GSGlyph(CJK_GUIDE_GLYPH))
			print('[CJK Metrics Info]: Add glyph \'{}\'!'.format(CJK_GUIDE_GLYPH))

			layerWidth = 1000.0
			for param in filter(lambda x: x.name == 'Default Layer Width', font.customParameters):
				split = param.value.split(':')
				if len(split) == 1:
					layerWidth = toFloat(split[0])
				else:
					if split[0].strip() == 'han':
						layerWidth = toFloat(split[1])

			for layer in font.glyphs[CJK_GUIDE_GLYPH].layers:
					layer.width = layerWidth

		cjkGuideGlyph = font.glyphs[CJK_GUIDE_GLYPH]
		cjkGuideGlyph.export = False
		cjkGuideGlyph.storeScript = True
		cjkGuideGlyph.script = 'han'

	@objc.python_method
	def drawTripartiteDivisionLines(self, layer):
		'''Draw the tripartite division lines (三等分线).'''
		scale = self.getScale()

		view = Glyphs.font.currentTab.graphicView()
		visibleRect = view.visibleRect()
		activePosition = view.activePosition()

		viewOriginX = (visibleRect.origin.x - activePosition.x) / scale
		viewOriginY = (visibleRect.origin.y - activePosition.y) / scale
		viewWidth = visibleRect.size.width / scale
		viewHeight = visibleRect.size.height / scale

		height = layer.ascender - layer.descender
		width  = layer.width

		# Calculate positions for tripartite division based on the basis percentage
		basis_width = width * self.tripartiteDivisionBasis / 100
		basis_height = height * self.tripartiteDivisionBasis / 100

		third_width = basis_width / 3
		third_height = basis_height / 3

		# Calculate the center of the glyph
		center_x = width / 2
		center_y = (layer.ascender + layer.descender) / 2

		# TODO: color
		color = NSColor.systemBlueColor()
		color.set()

		path = NSBezierPath.bezierPath()
		path.setLineDash_count_phase_([5.0, 2.0], 2, 0.0)  # Set dashed line

		# Vertical lines
		for i in range(1, 3):
			x = center_x - basis_width / 2 + i * third_width
			path.moveToPoint_((x, viewOriginY))
			path.lineToPoint_((x, viewOriginY + viewHeight))

		# Horizontal lines
		for i in range(1, 3):
			y = center_y - basis_height / 2 + i * third_height
			path.moveToPoint_((viewOriginX, y))
			path.lineToPoint_((viewOriginX + viewWidth, y))

		path.setLineWidth_(1 / scale)
		path.stroke()

	@objc.python_method
	def __file__(self):
		'''Please leave this method unchanged'''
		return __file__


def toFloat(s):
	'''Safely convert a string to float number.'''
	try:
		return float(s)
	except ValueError:
		return 0.0
